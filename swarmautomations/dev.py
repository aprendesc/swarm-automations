from dotenv import dotenv_values
env_vars = dotenv_values('C:\\Users\\AlejandroPrendesCabo\\Desktop\\.env')
aux = str(env_vars)
eval(aux)

def save_env_dict(env_vars, filepath=".env"):
    with open(filepath, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
save_env_dict(env_vars, filepath=".env")