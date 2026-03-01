import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NotificationService } from '../app/core/services/notification';
import { ConfirmService } from './core/services/confirm';
import { ViewProductService } from './core/services/view-product.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  public notify = inject(NotificationService);
  public confirmSrv = inject(ConfirmService);
  public viewSrv = inject(ViewProductService);
}
