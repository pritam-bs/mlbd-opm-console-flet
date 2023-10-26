from ....data.model.synchronizer.model_update_dto import ModelUpdateDTO, NewUserDTO
from ....domain.entities.model_update_entity import ModelUpdateEntity, NewUserEntity


class ModelUpdateRemapper:
    @staticmethod
    def map(new_user_dto: NewUserDTO):
        return NewUserEntity(employee_id=new_user_dto.employee_id)

    @staticmethod
    def map_sqs_dto(model_update_dto: ModelUpdateDTO):
        new_users_entity = [ModelUpdateRemapper.map(user)
                            for user in model_update_dto.onboarded_users]
        entity = ModelUpdateEntity(new_employee_list=new_users_entity)
        return entity
