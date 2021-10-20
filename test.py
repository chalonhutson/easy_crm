from werkzeug.security import check_password_hash

result = check_password_hash("pbkdf2:sha256:260000$gbIJ2lM5LefO7Hk7$84c0cd440839b2a1fb7fafdeaafd7d3ccda82ba7956fdd747352803fb3bb4229", "password1234")

print(result)