from django.contrib import admin
from TigerTutorsApp.models import Discover, Member, MathematicsDocument, PhysicsDocument, ComputerDocument, \
     TeamMember
from TigerTutorsApp.models import Contact



# Register your models here.
admin.site.register(Discover)
admin.site.register(Contact)
admin.site.register(Member)
admin.site.register(MathematicsDocument)
admin.site.register(PhysicsDocument)
admin.site.register(ComputerDocument)
admin.site.register(TeamMember)
