from apps.discogs_survey_experiment.discogs_survey_aol_experiment import DiscogsSurveyAOLExperiment
from apps.discogs_survey_experiment.discogs_survey_musicbrainz_experiment import DiscogsSurveyMBExperiment


experiment_aol = DiscogsSurveyAOLExperiment("files\\aol_result_buscador_discogs.tsv")
# print experiment.run()
experiment_mb = DiscogsSurveyMBExperiment("files\\musicbrainz_result_buscador_discogs.tsv")
print experiment_mb.run()