import { API_BASE_URL } from "../api/client";


function ProductCard({ product, onSelect }) {
  const isAvailable = product.stock > 0;

  return (
    <article
      className={`product-card ${
        !isAvailable ? "product-card-unavailable" : ""
      }`}
    >
      <div className="product-card-image">
        {product.image_url ? (
          <img
            src={`${API_BASE_URL}${product.image_url}`}
            alt={product.name}
          />
        ) : (
          <div className="product-image-placeholder">
            <span>
              {product.category === "headphones"
                ? "🎧"
                : "▣"}
            </span>
          </div>
        )}

        <span
          className={`availability-badge ${
            isAvailable
              ? "availability-available"
              : "availability-unavailable"
          }`}
        >
          {isAvailable ? "In stock" : "Unavailable"}
        </span>
      </div>

      <div className="product-card-body">
        <div className="product-category">
          {product.category}
        </div>

        <h3>{product.name}</h3>

        <p>{product.description}</p>

        <div className="product-card-price">
          <strong>
            ₹{Number(product.price).toLocaleString("en-IN")}
          </strong>

          {product.rating && (
            <span>
              ★ {product.rating}
            </span>
          )}
        </div>

        <div className="product-card-meta">
          {product.features?.anc && (
            <span>ANC</span>
          )}

          {product.features?.wireless && (
            <span>Wireless</span>
          )}

          {product.features?.battery_hours && (
            <span>
              {product.features.battery_hours}h battery
            </span>
          )}
        </div>

        <div className="product-card-footer">
          <span>
            {isAvailable
              ? `${product.stock} available`
              : "Currently unavailable"}
          </span>

          <button
            type="button"
            onClick={() => onSelect(product)}
            disabled={!isAvailable}
          >
            {isAvailable
              ? "View details →"
              : "Unavailable"}
          </button>
        </div>
      </div>
    </article>
  );
}

export default ProductCard;