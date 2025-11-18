import { Component, inject } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import { BackendService } from './services/backend.service';
import { Activity } from './models/activity';
import { Weather } from './models/weather';
import { CardComponent } from './components/card/card.component';
import { SpinnerComponent } from "./components/loading-spinner/loading-spinner.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    CommonModule,
    FormsModule,
    MatIconModule,
    CardComponent,
    SpinnerComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  place = '';
  backendService = inject(BackendService);
  activities: Activity[] = [];
  weather: Weather | null = null;
  showSpinner = false;

  async explore() {
   this.activities = [];
   this.weather = null;
   this.showSpinner = true;
   
   const result = await this.backendService.getRecommendations(this.place);
   this.activities = result.activities;
   this.weather = result.weather;
   
   this.showSpinner = false;
  }


}
