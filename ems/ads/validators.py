from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """ Валидация расширения файлов """
    extension = value.name.split('.')[-1]
    valid_extensions = ['pdf', 'doc', 'docx', 'jpg',
                        'png', 'xlsx', 'xls', 'pptx', 'txt', 'csv', 'md', 'ppt']
    if not extension.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension: ({value.name})')
    return value


def validate_file_size(value):
    """ Валидация размера файла """
    limit = 1024 * 1024 * 10
    if value.size > limit:
        raise ValidationError(f'File too large. Size should not exceed 10 MB')
    return value
