from ....data.model.synchronizer.model_change_dto import ModelChangeDTO
from ....domain.entities.model_change_entity import ModelChangeEntity


class ModelChangeRemapper:
    @staticmethod
    def map_from(model_change_dto: ModelChangeDTO):
        return ModelChangeEntity(
            employee_id=model_change_dto.employee_id)

    @staticmethod
    def map_to(model_change_entity: ModelChangeEntity):
        return ModelChangeDTO(
            employee_id=model_change_entity.employee_id)
