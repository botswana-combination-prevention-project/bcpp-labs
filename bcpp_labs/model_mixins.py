from bcpp_status import StatusHelper
from django.db import models
from edc_lab.model_mixins.requisition import RequisitionIdentifierMixin
from edc_lab.model_mixins.requisition import RequisitionModelMixin, RequisitionStatusMixin
from edc_map.site_mappers import site_mappers
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_reference.model_mixins import RequisitionReferenceModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin
from edc_visit_tracking.model_mixins import PreviousVisitModelMixin


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class MyUpdatesRequisitionMetadataModelMixin(UpdatesRequisitionMetadataModelMixin):

    status_helper_cls = StatusHelper

    def run_metadata_rules_for_crf(self):
        """Runs all the rule groups for this app label.

        Inserts a call to the status helper.
        """
        self.status_helper_cls(visit=self.visit, update_history=True)
        super().run_metadata_rules_for_crf()

    class Meta:
        abstract = True


class SubjectRequisitionModelMixin(
        RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin,
        VisitTrackingCrfModelMixin, OffstudyMixin,
        PreviousVisitModelMixin, RequisitionReferenceModelMixin,
        MyUpdatesRequisitionMetadataModelMixin, models.Model):

    objects = Manager()

    def save(self, *args, **kwargs):
        self.study_site = site_mappers.current_map_code
        self.study_site_name = site_mappers.current_map_area
        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = [
            'requisition_identifier',
            'subject_identifier',
            'human_readable_identifier',
            'panel_name',
            'panel_object.abbreviation',
            'identifier_prefix']
        return fields

    class Meta:
        abstract = True

#     class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
#         consent_model = 'bcpp_subject.subjectconsent'
#         app_label = 'bcpp_subject'
#         anonymous_consent_model = 'bcpp_subject.anonymousconsent'
