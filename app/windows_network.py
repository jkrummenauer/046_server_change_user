import subprocess
from dataclasses import dataclass
from .config import NETWORK_PATH, DOMAIN


@dataclass
class CommandResult:
    success: bool
    output: str


def run_command(command: list[str]) -> CommandResult:
    """
    Executa um comando no Windows e retorna o resultado.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,
            encoding="cp850",
            errors="replace",
        )

        output = result.stdout.strip() or result.stderr.strip()

        return CommandResult(
            success=result.returncode == 0,
            output=output,
        )

    except Exception as error:
        return CommandResult(
            success=False,
            output=f"Erro ao executar comando: {error}",
        )


def normalize_server_from_path(network_path: str) -> str:
    """
    Extrai o servidor de um caminho como:
    \\\\SERVIDOR\\Compartilhamento
    \\\\192.168.0.10\\Pasta
    """
    cleaned = network_path.strip().replace("/", "\\")

    if not cleaned.startswith("\\\\"):
        raise ValueError("O caminho deve começar com \\\\, exemplo: \\\\SERVIDOR\\Pasta")

    parts = cleaned.strip("\\").split("\\")

    if not parts:
        raise ValueError("Caminho de rede inválido.")

    return parts[0]


def remove_existing_connection(network_path: str) -> CommandResult:
    """
    Remove conexão existente com o compartilhamento.
    """
    return run_command(["net", "use", network_path, "/delete", "/y"])


def remove_saved_credentials(server: str) -> CommandResult:
    """
    Remove credenciais salvas no Windows Credential Manager.
    """
    return run_command(["cmdkey", f"/delete:{server}"])


def connect_to_network_share(
    network_path: str,
    username: str,
    password: str,
) -> CommandResult:
    """
    Conecta ao compartilhamento de rede com usuário e senha.
    """
    network_path = NETWORK_PATH
    domain = DOMAIN

    if domain:
        full_username = f"{domain}\\{username}"
    else:
        full_username = username

    return run_command(
        [
            "net",
            "use",
            network_path,
            password,
            f"/user:{full_username}",
            "/persistent:no",
        ]
    )


def switch_server_user(
    username: str,
    password: str,
    ) -> CommandResult:
    """
    Troca o usuário de acesso a um compartilhamento de rede.
    """
    try:
        server = normalize_server_from_path(NETWORK_PATH)
    except ValueError as error:
        return CommandResult(False, str(error))

    remove_existing_connection(network_path)
    remove_saved_credentials(server)

    connection_result = connect_to_network_share(
        network_path=network_path,
        username=username,
        password=password,
        domain=domain,
    )

    if connection_result.success:
        return CommandResult(
            True,
            f"Conexão realizada com sucesso em {network_path}.",
        )

    return CommandResult(
        False,
        f"Não foi possível conectar.\n\nDetalhes:\n{connection_result.output}",
    )


def list_network_connections() -> CommandResult:
    """
    Lista conexões de rede ativas.
    """
    return run_command(["net", "use"])
