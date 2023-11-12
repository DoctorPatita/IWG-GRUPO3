from django import forms

from blog.models import BlogPost, Comment


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		return blog_post
	
class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['body']

class AddCommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['body']
		widgets = {
			'body': forms.Textarea(attrs={'class': 'form-control'}),
		}