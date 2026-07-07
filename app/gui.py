import customtkinter as ctk
from tkinter import messagebox

from app.windows_network import (
    switch_server_user,
    list_network_connections,
)


class ServerAccessApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Acesso - Servidor")

        largura_janela = 400
        altura_janela = 350

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = int((largura_tela - largura_janela) / 2)
        pos_y = int((altura_tela - altura_janela) / 2)

        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.resizable(False, False)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self._build_layout()

    def _build_layout(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Troca Acesso ao Servidor",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title.pack(pady=(25, 10))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=30, pady=10, fill="x")

        self.username_entry = self._add_input(
            form_frame,
            label="Usuário",
            placeholder="Digite o usuário",
        )

        self.password_entry = self._add_input(
            form_frame,
            label="Senha",
            placeholder="Digite a senha",
            show="*",
        )

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(padx=30, pady=15, fill="x")

        connect_button = ctk.CTkButton(
            button_frame,
            text="Trocar usuário",
            height=40,
            command=self._on_switch_user,
        )
        connect_button.pack(side="left", expand=True, fill="x", padx=(0, 8))

        list_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            height=40,
            command=self._cancelar,
        )
        list_button.pack(side="left", expand=True, fill="x", padx=(8, 0))

        self.output_box = ctk.CTkTextbox(self, height=150)
        self.output_box.pack(padx=30, pady=(10, 20), fill="both")
        self.output_box.insert("1.0", "Status do sistema aparecerá aqui.")
        self.output_box.configure(state="disabled")

    def _add_input(
        self,
        parent: ctk.CTkFrame,
        label: str,
        placeholder: str,
        show: str | None = None,
    ) -> ctk.CTkEntry:
        label_widget = ctk.CTkLabel(
            parent,
            text=label,
            anchor="w",
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        label_widget.pack(padx=20, pady=(12, 2), fill="x")

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=36,
            show=show,
        )
        entry.pack(padx=20, pady=(0, 6), fill="x")

        return entry

    def _write_output(self, text: str) -> None:
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.configure(state="disabled")

    def _validate_fields(self) -> bool:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:
            messagebox.showwarning(
                "Campo obrigatório",
                "Informe o usuário.",
            )
            return False

        if not password:
            messagebox.showwarning(
                "Campo obrigatório",
                "Informe a senha.",
            )
            return False

        return True

    def _on_switch_user(self) -> None:
        if not self._validate_fields():
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        self._write_output("Alterando conexão...")

        result = switch_server_user(
            username=username,
            password=password,
        )

        self._write_output(result.output)

        if result.success:
            messagebox.showinfo("Sucesso", result.output)
        else:
            messagebox.showerror("Erro", result.output)

    def _cancelar(self) -> None:
        self.destroy()

if __name__ == "__main__":
    ServerAccessApp().mainloop()
