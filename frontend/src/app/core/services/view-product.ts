import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ViewProductService {
  private displaySignal = signal<boolean>(false);
  private productSignal = signal<any>(null);

  public display = this.displaySignal.asReadonly();
  public product = this.productSignal.asReadonly();

  open(product: any) {
    this.productSignal.set(product);
    this.displaySignal.set(true);
  }

  close() {
    this.displaySignal.set(false);
    this.productSignal.set(null);
  }
}
