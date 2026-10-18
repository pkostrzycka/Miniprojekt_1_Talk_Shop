# =====================================================================================
#                                     IMPORTS
# =====================================================================================
import argparse
from lark import Lark, Token, Tree
from dataclasses import dataclass

# ======================================================================================
#                                     DATA MODEL
# ======================================================================================
@dataclass
class Product:
    name: str
    price: float
    stock: int


products: dict[str, Product] = {
    "monorail": Product(name="Monorail", price=1449.99, stock=30),
    "hewlett_packard": Product(name="Hewlett Packard", price=1849.99, stock=23),
    "compaq": Product(name="COMPAQ", price=2399.99, stock=8),
}

# =====================================================================================
#                                      NLP
# =====================================================================================

#
# How much is the jacket
#
#


def pretty_print(node: Tree|Token, depth: int=0)->None:
    if isinstance(node, Token):
        print("  "*depth + f"{node.type} = {node}")
        return
    print("  "*depth + node.data)
    for subtree in node.children:
        pretty_print(subtree, depth+1)
    

def process_query(query: str, parser: Lark) -> str:
    tree = parser.parse(query.lower().strip())

    query_node = tree.children[0]

    if not isinstance(query_node, Tree):
        return "Unable to process query."

    # Znajdujemy produkt w pytaniu
    item_tokens = list(query_node.scan_values(
        lambda value: isinstance(value, Token)
        and value.type == "ITEM"
    ))

    if not item_tokens:
        return "Product not found in question."

    item = str(item_tokens[0])

    # Sprawdzamy, czy produkt istnieje w sklepie
    if item not in products:
        return f"Sorry, we don't sell {item}."

    product = products[item]

    # Pytanie o cenę
    if query_node.data == "price_question":
        return f"The {product.name} costs {product.price}$"

    # Pytanie o dostępność
    elif query_node.data == "availability_question":
        if product.stock > 0:
            return f"Yes, {product.name} is available."
        else:
            return f"No, {product.name} is out of stock."

    # Pytanie o liczbę sztuk
    elif query_node.data == "stock_question":
        return f"We have {product.stock} units of {product.name} in stock."

    return "Unable to process query."

# =====================================================================================
#                                        MAIN
# =====================================================================================
def main() -> None:
    argumenty = argparse.ArgumentParser(
        description="Shop chatbot"
    )

    argumenty.add_argument(
        "-g",
        "--grammar",
        default="grammar.txt",
        help="Path to grammar file"
    )

    args = argumenty.parse_args()

    try:
        with open(args.grammar, "r", encoding="utf-8") as plik:
            grammar = plik.read()

        parser = Lark(grammar, parser="earley")

    except Exception as error:
        print(f"Cannot load grammar: {error}")
        return

    while True:
        try:
            query = input("Query: ")

            if query.strip().upper() == "END":
                print("Goodbye!")
                break

            response = process_query(query, parser)
            print(response)

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        except Exception as error:
            print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()