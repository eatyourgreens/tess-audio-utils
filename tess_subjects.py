from subject_utils import fetch_light_curve, light_curve_url, normalise_light_curve, sonify
from panoptes_client import SubjectSet
from pathlib import Path

subject_set = SubjectSet.find(117755)
i = 1

Path('wav/sims').mkdir(parents=True, exist_ok=True)

for subject in subject_set.subjects:
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
  fname = f"wav/sims/{subject.id}.wav"
  soni.save(fname)
  i = i + 1