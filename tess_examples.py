from subject_utils import fetch_light_curve, light_curve_url, normalise_light_curve, sonify
from panoptes_client import Subject


EXAMPLES = [85751621, 85754178, 85750107, 85753189, 85752142, 85772758, 85772755, 85753402, 85749125, 85752601, 85748425]
i = 1

for subject_id in EXAMPLES:
  subject = Subject.find(subject_id)
  url = light_curve_url(subject)
  print(i, url)
  days, fluxes = fetch_light_curve(url)
  x, y = normalise_light_curve(days, fluxes)

  data = {'pitch':1.,
          'time_evo':x,
          'azimuth':(x*0.5+0.25) % 1,
          'polar':0.5,
          'pitch_shift':(y*10+1)**-0.7}

  soni = sonify(data)
  soni.render()
  fname = f"wav/examples/{subject.id}.wav"
  soni.save(fname)
  i = i + 1
