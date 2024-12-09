from django.contrib import admin
from TigerTutorsApp.models import Discover, Member, Admin, MathematicsDocument, PhysicsDocument, ComputerDocument, \
    Document, TeamMember
from TigerTutorsApp.models import Contact



# Register your models here.
admin.site.register(Admin)
admin.site.register(Discover)
admin.site.register(Contact)
admin.site.register(Member)
admin.site.register(MathematicsDocument)
admin.site.register(PhysicsDocument)
admin.site.register(ComputerDocument)
admin.site.register(Document)
admin.site.register(TeamMember)
