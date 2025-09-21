# Wheels Next The Sea

A Django-based website for **Wheels Next The Sea**, a motorcycle festival.  
This project includes apps for managing events, gallery images, reviews, and contact information.

---

## Repository Structure

### Apps

#### 1. **Events**
- Handles **Upcoming** and **Past Events**
- Event fields:
  - `title`, `description`, `date`
  - `flyer` (image upload)
  - `folder` (links to gallery folder)
- Features:
  - Upcoming and past event pages
  - Delete events (staff-only) with redirect to correct page
  - Flyer modal image preview
  - Button linking events to their corresponding gallery year

#### 2. **Gallery**
- Organized by **year folders**
- Each folder contains multiple images
- Features:
  - Boxed layout by year (4 preview images per box)
  - Clicking opens full gallery view
  - Modal viewer with navigation and thumbnails
  - Superuser can upload, edit, and delete images/folders
  - JPEGs converted to **WebP** for performance

#### 3. **Reviews**
- Stores user-submitted reviews
- Reviews are displayed on the reviews page
- Reviews also scroll as a marquee on the homepage
- Features:
  - Review submission form
  - Staff can delete reviews
  - Review moderation workflow (via admin)

#### 4. **Contact**
- Stores site contact information:
  - `address`, `phone`, `email`
- `ContactNotification`:
  - Many-to-many field linking **staff users** who should receive form submissions
- Contact form:
  - Sends email notifications to configured staff
  - Includes secure reply link with token

---

## Templates

- **Base layout**: `base.html` with navigation and footer
- **Events templates**:
  - `current-events.html` (Upcoming)
  - `past-events.html` (Past)
- **Gallery templates**:
  - `gallery.html` (year previews)
  - `year_gallery.html` (full year view with modal)
- **Reviews templates**:
  - `reviews.html`
  - Review marquee on homepage
- **Contact template**:
  - `contact.html` with form
- **Auth templates**:
  - Styled login form with "Remember me" checkbox
  - Forgot password link

---

## Static / Styling

- Global styles with dark gradient background
- `auth-card` styling for login/register pages
- Buttons:
  - `.btn-primary` (red)
  - `.btn-danger` (outlined red)
- Event cards styled with images and action buttons
- Gallery modal for images
- Mobile menu:
  - Dropdown positioned on the right
  - Modal-style overlay
  - Auto closes on outside click

---

## Admin

- Manage **Events**, **Reviews**, **Gallery folders & images**, **Contact info**
- Staff-only recipient selection for contact notifications
- Superuser/staff permissions enforced on sensitive actions
- Contact admin shows which staff users are in the recipient list

---

## Deployment Notes

- Deployed on **Heroku**
- Uses environment variables for sensitive settings (`SECRET_KEY`, `EMAIL_HOST_USER`, etc.)
- `.env` is not committed
- Error logging shows `.env` probes are safely rejected (404)

---

## Features Summary

- 🔴 Upcoming & Past events with flyers and galleries  
- 🖼️ Gallery by year with modal viewer  
- 📝 Reviews with scrolling homepage display  
- 📬 Contact form with staff notifications  
- 🔐 Staff-only deletion & admin tools  
- 📱 Mobile-friendly navigation & styling  

---

## Credits

Developed and maintained by **Viktor Mathe**  
Website: [wheelsnextthesea.co.uk](https://wheelsnextthesea.co.uk)