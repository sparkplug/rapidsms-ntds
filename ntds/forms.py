
from django import forms

from generic.forms import FilterForm,ActionForm
from .utils import ExcelResponse
from rapidsms.contrib.locations.models import Location
from django.utils.safestring import mark_safe

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Mission Excel File',
                                 required=True)


class DownloadForm(ActionForm):
    action_label = 'Download Selected'



    def perform(self, request, results):
        headers = ["Name", "Mobile", "Created", "Age","district","gender"]







        data = results.values_list('name','connection__identity' ,'created', 'birthdate',
                                   'district','gender').iterator()
        if data:

            response = ExcelResponse(data=data,headers=headers)
        else:
            response = ExcelResponse(data=headers,headers=headers)


        return None,response


class SMSInput(forms.Textarea):
    """ A widget for sms input """

    def __init__(self, *args, **kwargs):
        super(SMSInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        javascript = """
         <script type="text/javascript">
            //<![CDATA[
            function count_characters(name,counter_container,submit_btn)
        {

        var el="[name='"+name+"']"

        var elem= $(el);

        var value = elem.val();
        var count = value.length;
        //regex for stripping the spaces
        var regex = new RegExp(/^\s*|\s*$/g);
        var chars_left = 160 - count;
        if (chars_left >= 0) {
          if (elem.is('.overlimit')) {
            elem.removeClass("overlimit");
          }

          if (chars_left > 1) {
            str = (chars_left) + " characters left";
          }
          else if (chars_left > 0) {
            str = "1 character left";
          }
          else {
            str = "No characters left";
          }
        } else {
          if (!elem.is('.overlimit')) {
            elem.addClass("overlimit");
          }

          if (chars_left < -1) {
            str = -chars_left + " characters over limit";
          }
          else {
            str = "1 character over limit";
          }
        }
        var ok = (count > 0 && count < 161) && (value.replace(regex,"") != elem._value);

        $(submit_btn).disabled = !ok;
        elem.next().html(str);
        }
        $(".smsinput").change(setInterval(function() {count_characters('%(name)s','.counter','foo');},500));

             //]]>
        </script>

        """%{'name':name}
        style = """
        width: 18em;
        height: 56px;
        border: 1px solid #CCCCCC;
        color: #222222;
        font: 14px/18px "Helvetica Neue",Arial,sans-serif;
        outline: medium none;
        overflow-x: hidden;
        overflow-y: auto;
        padding: 2px;
        white-space: pre-wrap;
        word-wrap: break-word;

        """
        attrs = {'style':style}
        attrs['class'] = "smsinput input-xxlarge"
        return mark_safe(
            "%s<div class='counter' ></div>" % super(SMSInput, self).render(name, value, attrs) + javascript)


class FreeSearchForm(FilterForm):

    """ concrete implementation of filter form
        TO DO: add ability to search for multiple search terms separated by 'or'
    """

    searchx = forms.CharField(max_length=100, required=False, label="",widget=forms.TextInput(attrs={'placeholder': 'Search'})
    )

    def filter(self, request, queryset):
        searchx = self.cleaned_data['searchx'].strip()
        if searchx == "":
            return queryset
        elif searchx[0] in ["'", '"'] and searchx[-1] in ["'", '"']:
            searchx = searchx[1:-1]
            return queryset.filter(Q(name__iregex=".*\m(%s)\y.*" % searchx)
                                   | Q(location__iregex=".*\m(%s)\y.*" % searchx)
                                   | Q(connection__identity__iregex=".*\m(%s)\y.*" % searchx))

        else:
            return queryset.filter(Q(name__icontains=searchx)
                                   | Q(location__icontains=searchx)
                                   | Q(connection__identity__icontains=searchx))

class MultipleDistictFilterForm(FilterForm):

    districts = forms.ModelMultipleChoiceField(queryset=
                                               Location.objects.filter(type__slug='district'
                                               ).order_by('name'), required=False,help_text="Filter By District")


    def filter(self, request, queryset):

        districts = Location.objects.filter(pk__in=self.cleaned_data['districts']).values_list("name",flat=True)
        if len(districts):
            return queryset.filter(pk__in=queryset).filter(reduce(operator.or_, (Q(location__contains=x) for x in districts)))
        else:
            return queryset


class SendTextForm(ActionForm):
    text = forms.CharField(required=True, widget=SMSInput())
    action_label = 'Send SMS'


    def perform(self, request, results):
        if results is None or len(results) == 0:
            return ('A message must have one or more recipients!',
                    'error')
        text = self.cleaned_data['text']
        router = get_router()
        connections=Connection.objects.filter(pk__in=results.values_list("connection__pk").distinct())
        for conn in connections:
            router.add_outgoing(conn, text)


        return ('SMS  sent to %d People' % results.count(),
                'success')


