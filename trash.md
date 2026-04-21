what is the diffence between them?:-

app.config['SECRET_KEY']='your_secret_key'
app.secret_key = "super_secret_key_here"
which one is correct?


what does this means:-
app.config["SECRET_KEY"] = "IF I WROTE THIS THEN WHAT IS THE MEANING OF THIS ?"

how flash works

To actually see the flash message, you need to use a template (.html file) and a special Flask function called get_flashed_messages().



These are the Bootstrap utility classes used across your templates. Be prepared to explain what each category does:

Layout (Grid System)
Class	What it does
container	Centers content with fixed max-width
row	Creates a horizontal flex row
col-md-3, col-md-6, col-md-9, col-lg-5	Responsive column widths (12-column grid)
justify-content-center	Centers columns horizontally
Navigation
Class	What it does
navbar, navbar-expand-lg	Responsive navbar, expands at lg breakpoint
navbar-dark, bg-primary	Dark text icons + blue background
navbar-toggler	Hamburger button for mobile
navbar-nav, nav-item, nav-link	Nav list items and links
ms-auto	Pushes nav items to the right (margin-start: auto)
Cards
Class	What it does
card, card-body, card-header, card-footer	Bootstrap card component
shadow-sm	Small drop shadow
border-0	Removes card border
card-title, card-subtitle, card-text	Text inside cards
Buttons
Class	What it does
btn btn-primary	Filled blue button
btn btn-outline-primary/secondary/danger/success	Outlined buttons
btn btn-sm, btn btn-lg	Small/large button sizes
btn-close	X close button (used in alerts)
Forms
Class	What it does
form-control	Styled input/textarea
form-label	Styled label
form-select, form-select-sm	Styled <select> dropdown
d-grid	Makes button full-width
mb-3, mb-4	Bottom margin spacing
Tables
Class	What it does
table	Base table style
table-hover	Highlights row on hover
table-light	Light grey <thead>
table-responsive	Adds horizontal scroll on small screens
align-middle	Vertically centers cell content
Badges & Alerts
Class	What it does
badge bg-success/danger/info/warning/secondary	Colored status badges
alert alert-{{ category }}	Flash message alerts
alert-dismissible fade show	Dismissible animated alert
Utilities
Class	What it does
text-primary, text-muted, text-dark, text-white	Text colors
fw-bold	Font weight bold
d-flex, justify-content-between, align-items-center	Flexbox utilities
text-center	Center-aligns text
mt-2, mt-4, mt-5, me-2, p-5	Spacing utilities (margin/padding)
w-100	Width 100%
small	Smaller font size
rounded-circle	Makes image circular (student avatar)
vh-100	Height = 100% viewport height
gap-3	Gap between grid items
list-group, list-group-flush, list-group-item	Styled list component