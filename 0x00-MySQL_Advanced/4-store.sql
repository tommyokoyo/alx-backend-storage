-- Creates trigger that decreases the quantity of
-- an item after adding a new order
DELIMITER //

CREATE TRIGGER after_insert_order
AFTER INSERT ON orders FOR EACH ROW
BEGIN
    -- Update the quantity of the item in the items table
    UPDATE items
    SET quantity = quantity - NEW.quantity_ordered
    WHERE id = NEW.item_id;
END;
//

DELIMITER ;