import re

from rest_framework import serializers


def validate_sql_injection(value):
    sql_injection_patterns = [
        r";", r"--", r"/\*", r"xp_", r"drop\s", r"select\s",
        r"insert\s", r"delete\s", r"update\s", r"alter\s",
        r"exec\s", r"union\s",
    ]

    for pattern in sql_injection_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise serializers.ValidationError("Invalid characters detected in the input.")

    if not re.match(r'^[\w\s\-]+$', value):
        raise serializers.ValidationError("Only alphanumeric characters, spaces and hyphens are allowed.")

    return value