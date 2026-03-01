import { Injectable, signal } from '@angular/core';
import { BACKEND_MESSAGES } from '../utils/error-messages';

export interface Notification {
  message: string;
  type: 'success' | 'error' | 'info';
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notificationSignal = signal<Notification | null>(null);
  public notification = this.notificationSignal.asReadonly();

  translateAndShow(message: string, type: 'success' | 'error' | 'info' = 'success') {
    let translatedMessage = BACKEND_MESSAGES[message] || message;

    if (message.includes('does not exist')) {
      translatedMessage = message.replace('Product with ID', 'Produto com ID')
        .replace('User with ID', 'Usuário com ID')
        .replace('does not exist', 'não existe');
    }

    this.show(translatedMessage, type);
  }

  show(message: string, type: 'success' | 'error' | 'info' = 'success') {
    this.notificationSignal.set({ message, type });

    setTimeout(() => {
      this.clear();
    }, 3000);
  }

  clear() {
    this.notificationSignal.set(null);
  }
}
