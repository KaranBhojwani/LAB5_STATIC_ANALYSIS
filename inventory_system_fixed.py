"""
inventory_system_fixed.py

Refactored inventory management system for Lab 5:
- Add/remove products
- Load/save inventory
- Check low-stock items
- Demo operations
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("inventory_manager")

inventory: Dict[str, int] = {}


def add_product(name: str, qty: int, logs: Optional[List[str]] = None) -> bool:
    """Add a quantity of a product to the inventory and log the operation."""
    if logs is None:
        logs = []

    if not isinstance(name, str) or not name:
        logger.error("add_product: invalid name %r", name)
        return False

    if not isinstance(qty, int):
        logger.info(
            "add_product: qty must be int, got %r for %s", type(qty), name
        )
        return False

    if qty == 0:
        logger.warning("add_product: zero qty for %s", name)
        return True

    inventory[name] = inventory.get(name, 0) + qty
    entry = f"{datetime.now()}: Added {qty} of {name}"
    logs.append(entry)
    logger.info("%s", entry)
    return True


def remove_product(name: str, qty: int) -> bool:
    """Remove a quantity of a product from the inventory."""
    if not isinstance(name, str) or not name:
        logger.error("remove_product: invalid name %r", name)
        return False

    if not isinstance(qty, int) or qty <= 0:
        logger.error(
            "remove_product: qty must be positive int, got %r", qty
        )
        return False

    try:
        current = inventory.get(name)
        if current is None:
            logger.warning("remove_product: %s not found", name)
            return False

        if qty >= current:
            del inventory[name]
            logger.info(
                "remove_product: removed all of %s (was %d)", name, current
            )
        else:
            inventory[name] = current - qty
            logger.info(
                "remove_product: decreased %s by %d (now %d)",
                name,
                qty,
                inventory[name],
            )
        return True

    except KeyError as exc:
        logger.exception("remove_product: KeyError %s: %s", name, exc)
        return False


def get_stock(name: str) -> int:
    """Return current stock for a product, or 0 if not present or invalid."""
    if not isinstance(name, str) or not name:
        logger.error("get_stock: invalid name %r", name)
        return 0
    return inventory.get(name, 0)


def load_inventory(file: str = "inventory.json") -> bool:
    """Load inventory from a JSON file. Return True if successful."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            logger.error("load_inventory: bad format in %s", file)
            return False

        cleaned: Dict[str, int] = {}
        for k, v in data.items():
            if not isinstance(k, str):
                logger.warning(
                    "load_inventory: skipping non-str key %r", k
                )
                continue
            try:
                cleaned[k] = int(v)
            except (TypeError, ValueError):
                logger.warning(
                    "load_inventory: invalid qty for %s: %r", k, v
                )

        inventory.clear()
        inventory.update(cleaned)
        logger.info(
            "load_inventory: loaded %d items from %s", len(inventory), file
        )
        return True

    except FileNotFoundError:
        logger.warning(
            "load_inventory: %s not found, starting empty", file
        )
        inventory.clear()
        return False
    except json.JSONDecodeError as exc:
        logger.error(
            "load_inventory: JSON parse error in %s: %s", file, exc
        )
        return False
    except OSError as exc:
        logger.exception("load_inventory: I/O error %s: %s", file, exc)
        return False


def save_inventory(file: str = "inventory.json") -> bool:
    """Save current inventory to a JSON file. Return True if successful."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(inventory, f, indent=2)
        logger.info(
            "save_inventory: saved %d items to %s", len(inventory), file
        )
        return True
    except OSError as exc:
        logger.exception("save_inventory: I/O error %s: %s", file, exc)
        return False


def report_inventory() -> None:
    """Log the current inventory report."""
    logger.info("Inventory Report")
    if not inventory:
        logger.info("(empty inventory)")
        return
    for name, qty in inventory.items():
        logger.info("%s -> %d", name, qty)


def low_stock(limit: int = 5) -> List[str]:
    """Return a list of products with stock below the given limit."""
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be positive int")
    return [name for name, qty in inventory.items() if qty < limit]


def demo() -> None:
    """Demonstration of basic inventory operations."""
    logs: List[str] = []

    # Load existing inventory first
    load_inventory()

    add_product("apple", 10, logs)
    add_product("banana", 2, logs)
    add_product(123, 10, logs)
    add_product("mango", 0, logs)
    remove_product("apple", 3)
    remove_product("orange", 1)

    logger.info("Apple stock: %d", get_stock("apple"))
    logger.info("Low stock items: %s", low_stock())

    # Save updated inventory at the end
    save_inventory()
    report_inventory()


if __name__ == "__main__":
    demo()
