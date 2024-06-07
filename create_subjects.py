import os
from panoptes_client import Panoptes, Subject, SubjectSet
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = '7fecf1c5d5a2e1d7c9a6ccf0344e5ae9f1fb6ad7b412192d31182c6cdb3da8ed'
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
PROJECT_ID = 23238
SUBJECT_SET_ID = 121322

subject_set = SubjectSet.find(117755)
originals = subject_set.subjects

with Panoptes(client_id = CLIENT_ID, client_secret = CLIENT_SECRET):
  subject_set = SubjectSet.find(SUBJECT_SET_ID)
  subjects = []
  with Subject.async_saves():
    for original in originals:
      subject = Subject()
      subject.metadata.update(original.metadata)
      subject.metadata['!PH-TESS Subject'] = original.id
      subject.add_location(f'mp3/sims/{original.id}.mp3')
      subject.links.project = PROJECT_ID
      subject.save()
      subjects.append(subject)
  subject_set.add(subjects)
