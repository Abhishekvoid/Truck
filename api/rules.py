import rules
from .models import User



@rules.predicate
def is_company_x_staff(user,obj=None):

    if not user.is_authenticated:
        return False

    return user.role in [User.Role.COMPANY_X_ADMIN, User.Role.COMPANY_X_EMPLOYEE]

@rules.predicate
def is_org_manager(user, obj):

    if not user.is_authenticated or not hasattr(obj, 'organization'):
        return False

    return user.role == User.Role.ORG_MANAGER and user.organization == obj.organization


rules.add_rule('api.view_hmigroup', is_company_x_staff | is_org_manager)
rules.add_rule('api.change_hmigroup', is_company_x_staff | is_org_manager)
rules.add_rule('api.delete_hmigroup', is_company_x_staff | is_org_manager)


rules.add_rule('api.view_hmi', is_company_x_staff | is_org_manager)
rules.add_rule('api.change_hmi', is_company_x_staff | is_org_manager)
rules.add_rule('api.delete_hmi', is_company_x_staff | is_org_manager)

rules.add_rule('api.add_hmigroup', is_company_x_staff | is_org_manager)