from djoser import email

""" HTML-шаблоны для отправки писем на Email """


class PasswordResetEmail(email.PasswordResetEmail):
    
    """ Сброс пароля """
    
    template_name = 'email/password_reset.html'


class UsernameResetEmail(email.UsernameResetEmail):
    
    """ Сброс имени пользователя """
    
    template_name = 'email/username_reset.html'
