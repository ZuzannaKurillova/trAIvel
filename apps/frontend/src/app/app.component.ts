import { Component, inject } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

import { BackendService } from './services/backend.service';
import { ImageSearchService } from './services/image-search.service';
import { Activity } from './models/activity';
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
  imageSearch = inject(ImageSearchService);
  activities: Activity[] = [];
  showSpinner = false;

  async explore() {
   this.activities = [];
   this.showSpinner = true;
   this.activities = await this.backendService.getRecommendations(this.place);
   this.showSpinner = false;

   /*for(const [index, activity] of this.activities.entries()){
    this.activities[index].imgUrl = await this.imageSearch.getImage(this.place + activity.activity);
   }*/
  }


}
