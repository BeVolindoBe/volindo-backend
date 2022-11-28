from django.contrib import admin

from catalogue.models import Item

from agent.models import Agent


class AgentAdmin(admin.ModelAdmin):

    list_display = [
        'last_name',
        'first_name'
    ]
    search_fields = ['last_name', 'first_name']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['agent_status'].queryset = Item.objects.filter(
            catalogue__slug='agent_status'
        )
        context['adminform'].form.fields['country'].queryset = Item.objects.filter(
            catalogue__slug='countries'
        )
        context['adminform'].form.fields['phone_country_code'].queryset = Item.objects.filter(
            catalogue__slug='phone_country_codes'
        )
        return super(AgentAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Agent, AgentAdmin)
