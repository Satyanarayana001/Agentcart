import { useEffect, useState } from "react";

import { catalogApi } from "../api/client";
import ProductCard from "./ProductCard";
import ProductDetails from "./ProductDetails";

function ProductDiscovery({ onProductSelected }) {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] =
    useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProducts() {
      try {
        setLoading(true);
        setError("");

        const data = await catalogApi.getProducts();

        setProducts(data);
      } catch (err) {
        setError(
          err.message ||
            "Unable to load the product catalog."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  function handleSelectProduct(product) {
    onProductSelected(product);
  }

  return (
    <section className="product-discovery">

      <div className="discovery-header">
        <div>
          <div className="section-label">
            PRODUCT CATALOG
          </div>

          <h2>Explore available products</h2>

          <p>
            Browse the catalog or describe what you want
            above. AgentCart only recommends products that
            are currently available.
          </p>
        </div>

        <span className="catalog-count">
          {products.length} products
        </span>
      </div>

      {loading && (
        <div className="catalog-state">
          <div className="loading-indicator" />
          <span>Loading catalog...</span>
        </div>
      )}

      {error && (
        <div className="catalog-error">
          <strong>Catalog unavailable</strong>
          <span>{error}</span>
        </div>
      )}

      {!loading &&
        !error &&
        products.length === 0 && (
          <div className="catalog-state">
            <span>No products available.</span>
          </div>
        )}

      {!loading &&
        !error &&
        products.length > 0 && (
          <div className="product-grid">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onSelect={setSelectedProduct}
              />
            ))}
          </div>
        )}

      <ProductDetails
        product={selectedProduct}
        onClose={() => setSelectedProduct(null)}
        onSelect={handleSelectProduct}
      />
    </section>
  );
}

export default ProductDiscovery;