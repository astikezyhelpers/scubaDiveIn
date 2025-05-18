# Instructors Page Changes

## 1. Certification Section Changes

### Hero Section
- Remove "View Certifications" button from hero section
- Keep only "Book an Instructor" button

### Instructor Details
- Update certification badges to be identical for both instructors:
  * Nitrox Certified
  * Wreck Diving
  * Deep Diving
- Add "View Certificate" button in each instructor's detail section
- Add sample certificate image display functionality
  * Create modal popup for certificate display
  * Add sample certificate images (placeholder until client provides actual certificates)

## 2. Book an Instructor Form

### Model Creation
```python
class InstructorBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('closed', 'Closed')
        ],
        default='new'
    )
```

### Form Implementation
- Create popup modal form with fields:
  * Name (required)
  * Email (required)
  * Phone (required)
  * Preferred Date (required)
  * Message (optional)
- Add form validation
- Add success/error message handling

### Admin Panel
- Register model in admin.py
- Add list display fields:
  * Name
  * Email
  * Phone
  * Preferred Date
  * Status
  * Created At
- Add filters for Status and Created At
- Add search fields for Name, Email, and Phone

## 3. Reviews Section

### Changes
- Remove current testimonial section with arrows
- Replace with Google Reviews iframe from index.html
- Keep consistent styling with the page

### Code Snippet for Reviews
```html
<section class="py-16 bg-white">
  <div class="container mx-auto px-[5%]">
    <div class="text-center mb-16">
      <h2 class="text-3xl font-bold text-deep-blue mb-4">What Our Divers Say</h2>
      <p class="text-ocean-blue max-w-2xl mx-auto">Hear from certified divers who started their journey with us</p>
    </div>
    <iframe src='https://widgets.sociablekit.com/google-reviews/iframe/25558141' frameborder='0' width='100%' height='1000'></iframe>
  </div>
</section>
```

## Implementation Order
1. Remove hero section certification button
2. Update instructor certifications
3. Create InstructorBooking model
4. Implement booking form modal
5. Add certificate view functionality
6. Replace reviews section
7. Test all functionality
8. Add final styling adjustments

## Notes
- All changes will maintain existing color scheme and styling
- Will reuse existing components where possible
- Will maintain mobile responsiveness
- Will add proper error handling and validation 