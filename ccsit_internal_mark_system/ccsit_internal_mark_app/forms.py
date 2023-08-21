from django import forms

from ccsit_internal_mark_app.models import Marks, Feedback, Teacher, ElectiveCourse, ElectiveSubjectAllotment, \
    StudentRegistration, ElectiveSubject, ElectiveMarks, Send_Feedback


class CourseForm(forms.Form):
    course_name = forms.CharField(max_length=100)
    semester = forms.CharField(max_length=100)
    subjects = forms.CharField(widget=forms.Textarea)


class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['attendance', 'assignment', 'seminar', 'test1', 'test2']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Calculate the total marks
        total_marks = (
            instance.attendance +
            instance.assignment +
            instance.seminar +
            instance.test1 +
            instance.test2
        )
        instance.total_marks = total_marks

        if commit:
            instance.save()

        return instance

    def clean(self):
        cleaned_data = super().clean()
        attendance = cleaned_data.get('attendance')
        assignment = cleaned_data.get('assignment')
        seminar = cleaned_data.get('seminar')
        test1 = cleaned_data.get('test1')
        test2 = cleaned_data.get('test2')

        if attendance and attendance > 5:
            self.add_error('attendance', 'Attendance cannot exceed 5.')
        if assignment and assignment > 5:
            self.add_error('assignment', 'Assignment marks cannot exceed 5.')
        if seminar and seminar > 10:
            self.add_error('seminar', 'Seminar marks cannot exceed 10.')
        if test1 and test1 > 15:
            self.add_error('test1', 'Test 1 marks cannot exceed 15.')
        if test2 and test2 > 15:
            self.add_error('test2', 'Test 2 marks cannot exceed 15.')

        return cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['student_name','subject', 'internal_marks', 'message']
        widgets = {
            'internal_marks': forms.TextInput(attrs={'class': 'wide-input'}),
        }

class Send_Feedback_Form(forms.ModelForm):
    # teacher_name = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None, widget=forms.Select(attrs={'style': 'width: 75%;'}))

    class Meta:
        model = Send_Feedback
        fields = ['teacher_name', 'message']


class ElectiveCourseForm(forms.ModelForm):
    # Override the elective_subjects field to use a regular CharField
    elective_subjects = forms.CharField(label='Elective Subjects', help_text='Enter multiple subjects separated by commas.')

    class Meta:
        model = ElectiveCourse
        fields = ['course', 'semester', 'elective_subjects']


class ElectiveSubjectAllotmentForm(forms.ModelForm):
    class Meta:
        model = ElectiveSubjectAllotment
        fields = ['teacher', 'elective_subjects']
        widgets = {
            'elective_subjects': forms.CheckboxSelectMultiple(),
        }


class ElectiveMarksForm(forms.ModelForm):
    class Meta:
        model = ElectiveMarks
        fields = ['student', 'attendance', 'assignment', 'seminar', 'test1', 'test2','total_elective_marks']

ElectiveMarksFormSet = forms.modelformset_factory(
    ElectiveMarks, form=ElectiveMarksForm, extra=0
)


class ElectiveMarksForm(forms.Form):
    student_name = forms.CharField(label="Student Name", max_length=100)
    semester = forms.IntegerField(label="Semester")


