from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail


from config import settings
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('library:books_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в онлайн-библиотеку!' # Тема письма
        message = ('Здравствуйте! Благодарим вас за регистрацию в нашей онлайн-библиотеке.'
                   'Теперь вы можете: '
                   '• Просматривать каталог книг'
                   '• Читать описания и отзывы'
                   '• Создавать свои списки для чтения'
                   'Если у вас возникнут вопросы, пожалуйста, свяжитесь с нами.'
                   'С уважением, Команда онлайн-библиотеки')       # содержимое письма
        from_email = settings.DEFAULT_FROM_EMAIL    # адрес отправителя
        recipient_list = [user_email]       #  список получателей
        send_mail(subject, message, from_email, recipient_list)
