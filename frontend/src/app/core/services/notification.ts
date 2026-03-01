import { Injectable, signal } from '@angular/core';

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
