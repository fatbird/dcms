import base64
import imghdr
import logging
import six
import uuid

from django.conf import settings

from rest_framework import serializers

log = logging.getLogger('django.request')


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post
    data.  It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            extension = imghdr.what(file_name, decoded_file)
            if extension is None:
                self.fail('invalid_image')

            complete_file_name = "%s.%s" % (file_name, extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def to_representation(self, value):
        path = '%s%s' % (settings.MEDIA_ROOT, value)
        with open(path, 'rb') as image:
            encoded_string = base64.b64encode(image.read())
        extension = str(value).split('.')[-1]
        extension = 'jpeg' if extension.lower() == 'jpg' else extension.lower()
        return 'data:image/%s;base64,%s' % (extension, encoded_string)

