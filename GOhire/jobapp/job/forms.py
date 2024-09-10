from django import forms
from job.models import Job, Applicant, BookmarkJob

class JobForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"

        # Updating widget attributes
        placeholders = {
            'title': 'eg: Software Developer',
            'location': 'eg: Bangladesh',
            'salary': '$800 - $1200',
            'tags': 'Use comma separated. eg: Python, JavaScript',
            'last_date': 'YYYY-MM-DD',
            'company_name': 'Company Name',
            'url': 'https://example.com'
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder': placeholder})

    class Meta:
        model = Job
        fields = [
            "title", "location", "job_type", "category", "salary", 
            "description", "tags", "last_date", "company_name", 
            "company_description", "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')
        if not job_type:
            raise forms.ValidationError("Job Type is required.")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Category is required.")
        return category

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class joblyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['job']


class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['job']


class JobEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(JobEditForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Job Title :"
        self.fields['location'].label = "Job Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Job Description :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"

        # Updating widget attributes
        placeholders = {
            'title': 'eg: Software Developer',
            'location': 'eg: Bangladesh',
            'salary': '$800 - $1200',
            'last_date': 'YYYY-MM-DD',
            'company_name': 'Company Name',
            'url': 'https://example.com'
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({'placeholder': placeholder})

    class Meta:
        model = Job
        fields = [
            "title", "location", "job_type", "category", "salary", 
            "description", "last_date", "company_name", 
            "company_description", "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')
        if not job_type:
            raise forms.ValidationError("Job Type is required.")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Category is required.")
        return category

    def save(self, commit=True):
        job = super(JobEditForm, self).save(commit=False)
        if commit:
            job.save()
        return job
