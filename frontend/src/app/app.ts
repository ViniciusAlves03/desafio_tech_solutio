import { Component, inject } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NotificationService } from '../app/core/services/notification';
import { ConfirmService } from './core/services/confirm';
import { ViewProductService } from './core/services/view-product.service';
import { AuthService } from './core/services/auth';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  private authService = inject(AuthService);
  private router = inject(Router);
  public notify = inject(NotificationService);
  public confirmSrv = inject(ConfirmService);
  public viewSrv = inject(ViewProductService);

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
