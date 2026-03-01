import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ConfirmService {
  private displaySignal = signal<boolean>(false);
  private pendingAction: () => void = () => {};

  public display = this.displaySignal.asReadonly();
  public message = '';

  ask(message: string, onConfirm: () => void) {
    this.message = message;
    this.pendingAction = onConfirm;
    this.displaySignal.set(true);
  }

  confirm() {
    this.pendingAction();
    this.close();
  }

  close() {
    this.displaySignal.set(false);
  }
}
