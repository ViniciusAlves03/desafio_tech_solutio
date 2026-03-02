import { Component, inject, HostListener } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { NotificationService } from '../app/core/services/notification';
import { ConfirmService } from './core/services/confirm';
import { ViewProductService } from './core/services/view-product';
import { AuthService } from './core/services/auth';
import { UserService } from './core/services/user';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, ReactiveFormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  private authService = inject(AuthService);
  private userService = inject(UserService);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  public notify = inject(NotificationService);
  public confirmSrv = inject(ConfirmService);
  public viewSrv = inject(ViewProductService);

  isUserMenuOpen = false;
  showUserModal = false;
  userModalMode: 'view' | 'edit' = 'view';
  userData: any = null;
  userForm: FormGroup;

  constructor() {
    this.userForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.minLength(6)]]
    });
  }

  toggleUserMenu(event: Event) {
    event.stopPropagation();
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.closest('.user-menu-container')) {
      this.isUserMenuOpen = false;
    }
  }

  openUserModal(mode: 'view' | 'edit') {
    this.isUserMenuOpen = false;
    const userId = this.authService.getUserIdFromToken();
    if (!userId) return;

    this.userService.getUser(userId).subscribe({
      next: (user) => {
        this.userData = user;
        this.userModalMode = mode;
        if (mode === 'edit') {
          this.userForm.patchValue({
            username: user.username,
            email: user.email,
            password: ''
          });
        }
        this.showUserModal = true;
      },
      error: () => this.notify.show('Erro ao carregar dados da conta.', 'error')
    });
  }

  closeUserModal() {
    this.showUserModal = false;
    this.userData = null;
  }

  onUpdateUser() {
    if (this.userForm.invalid) {
      this.userForm.markAllAsTouched();
      return;
    }

    const userId = this.authService.getUserIdFromToken();
    if (!userId) return;

    const data = { ...this.userForm.value };
    if (!data.password) {
      delete data.password;
    }

    this.userService.updateUser(userId, data).subscribe({
      next: (updatedUser) => {
        this.userData = updatedUser;
        this.notify.show('Conta atualizada com sucesso!', 'success');
        this.closeUserModal();
      },
      error: (err) => {
        const rawMsg = err.error?.description || err.error?.message || 'Erro ao atualizar.';
        this.notify.translateAndShow(rawMsg, 'error');
      }
    });
  }

  confirmDeleteAccount() {
    this.isUserMenuOpen = false;
    this.confirmSrv.ask('Tem certeza que deseja excluir a sua conta? Esta ação é irreversível.', () => {
      const userId = this.authService.getUserIdFromToken();
      if (!userId) return;

      this.userService.deleteUser(userId).subscribe({
        next: () => {
          this.notify.show('Conta excluída com sucesso.', 'success');
          this.authService.removeToken();
          this.router.navigate(['/login']);
        },
        error: () => this.notify.show('Erro ao excluir conta.', 'error')
      });
    });
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => this.router.navigate(['/login']),
      error: () => this.router.navigate(['/login'])
    });
  }

  isLoggedIn(): boolean {
    return this.authService.isAuthenticated();
  }
}
