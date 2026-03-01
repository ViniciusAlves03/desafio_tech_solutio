import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import {NotificationService} from '../services/notification'

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private readonly TOKEN_KEY = 'jwt_token';

  constructor(private http: HttpClient, private notify: NotificationService) {}

  login(loginInput: string, passwordInput: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, {
      login: loginInput,
      password: passwordInput
    }).pipe(
      tap((response: any) => {
        if (response && response.access_token) {
          this.setToken(response.access_token);
        }
      })
    );
  }

  logout(): Observable<any> {
  return this.http.post(`${this.apiUrl}/auth/logout`, {}).pipe(
    tap(() => {
      this.removeToken();
      this.notify.show('Sessão encerrada com sucesso!', 'info');
    })
  );
}

  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    return token !== null && token.trim() !== '';
  }
}
