-- Adding products to the products table
INSERT INTO products (name, description, price, discount, stock, category_id, photo)
VALUES
    ('DETIP Hoodie', 'Official hoodie of the Department of Telecommunications and Informatics Engineering.', 29.99, 5, 100, 1, 'detip_hoodie.jpg'),
    ('DETIP Hat', 'Stylish hat with the DETIP logo embroidered.', 12.99, 0, 200, 2, 'detip_hat.jpg'),
	('DETI T-shirt', 'Official DETI T-shirt with the department logo.', 19.99, 0, 100, 1, 'deti_tshirt.jpg'),
    ('DETI Mug', 'Coffee mug featuring the DETI branding.', 9.99, 0, 150, 2, 'deti_mug.jpg'),
    ('DETI Backpack', 'Stylish backpack with multiple compartments for your tech gear.', 39.99, 5, 50, 3, 'deti_backpack.jpg'),
    ('DETI Sweatshirt', 'Warm and comfortable DETI Sweatshirt for the winter season.', 29.99, 0, 75, 1, 'deti_sweatshirt.jpg'),
    ('DETI Mousepad', 'High-quality mousepad with a DETI design.', 7.99, 0, 200, 4, 'deti_mousepad.jpg'),
    ('DETI USB Drive', 'Custom DETI-themed USB drive for your data storage needs.', 12.99, 0, 100, 5, 'deti_usb_drive.jpg'),
    ('DETI Notebook', 'Spiral-bound notebook with DETI branding for your notes.', 6.99, 0, 150, 6, 'deti_notebook.jpg'),
    ('DETI Poster', 'Decorate your room with a DETI poster featuring iconic images.', 8.99, 0, 50, 7, 'deti_poster.jpg');
-- Adding users
INSERT INTO users (first_name, last_name, email, password, type, city, country)
VALUES
    ('Admin', 'User', 'admin@example.com', 'admin_password', 'admin', 'Admin City', 'Admin Country'),
    ('Client', 'User', 'client@example.com', 'client_password', 'normal', 'Client City', 'Client Country');


-- adding categories
INSERT INTO categories (name)
VALUES
    ('Clothes'), -- For clothing items like T-shirts and hoodies
    ('Drinkware'), -- For items like mugs
    ('Computer Accessories'), -- For items like mousepads and USB drives
    ('Clothing Accessories'), -- For items like notebooks
    ('Decor'), -- For decorative items like posters
    ('Tech Accessories'), -- For tech-related accessories
    ('Promotional Items'); -- For promotional products