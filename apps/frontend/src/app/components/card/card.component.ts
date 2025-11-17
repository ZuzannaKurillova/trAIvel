import { Component, input } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Activity } from '../../models/activity';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [MatInputModule, MatButtonModule, CommonModule, FormsModule, MatIconModule, MatProgressSpinnerModule],
  templateUrl: './card.component.html',
  styleUrl: './card.component.scss'
})
export class CardComponent {
  activity = input<Activity>();
}
