function ProductDetails({
  product,
  onClose,
  onSelect,
}) {
  if (!product) {
    return null;
  }

  const isAvailable = product.stock > 0;

  return (
    <div className="product-details-overlay">
      <section className="product-details">

        <button
          type="button"
          className="product-details-close"
          onClick={onClose}
          aria-label="Close product details"
        >
          ×
        </button>

        <div className="product-details-grid">

          <div className="product-details-image">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.name}
              />
            ) : (
              <div className="product-image-placeholder large">
                <span>
                  {product.category === "headphones"
                    ? "🎧"
                    : "▣"}
                </span>
              </div>
            )}
          </div>

          <div className="product-details-content">

            <div className="product-category">
              {product.category}
            </div>

            <h2>{product.name}</h2>

            <p className="product-details-description">
              {product.description}
            </p>

            <div className="product-details-price">
              ₹{Number(product.price).toLocaleString("en-IN")}
            </div>

            {product.rating && (
              <div className="product-rating">
                <strong>
                  ★ {product.rating}
                </strong>

                {product.review_count && (
                  <span>
                    {product.review_count} reviews
                  </span>
                )}
              </div>
            )}

            <div className="product-detail-section">
              <span className="detail-section-label">
                FEATURES
              </span>

              <div className="feature-list">

                {product.features?.anc !== undefined && (
                  <div className="feature-item">
                    <span>Noise cancellation</span>
                    <strong>
                      {product.features.anc
                        ? "Active"
                        : "Not included"}
                    </strong>
                  </div>
                )}

                {product.features?.wireless !== undefined && (
                  <div className="feature-item">
                    <span>Wireless</span>
                    <strong>
                      {product.features.wireless
                        ? "Yes"
                        : "No"}
                    </strong>
                  </div>
                )}

                {product.features?.battery_hours && (
                  <div className="feature-item">
                    <span>Battery</span>
                    <strong>
                      {product.features.battery_hours} hours
                    </strong>
                  </div>
                )}

                {product.features?.water_resistant !== undefined && (
                  <div className="feature-item">
                    <span>Water resistant</span>
                    <strong>
                      {product.features.water_resistant
                        ? "Yes"
                        : "No"}
                    </strong>
                  </div>
                )}

                {product.features?.shock_protection !== undefined && (
                  <div className="feature-item">
                    <span>Shock protection</span>
                    <strong>
                      {product.features.shock_protection
                        ? "Yes"
                        : "No"}
                    </strong>
                  </div>
                )}

                {product.features?.extra_storage !== undefined && (
                  <div className="feature-item">
                    <span>Extra storage</span>
                    <strong>
                      {product.features.extra_storage
                        ? "Included"
                        : "No"}
                    </strong>
                  </div>
                )}

              </div>
            </div>

            <div className="product-stock">
              <span>Availability</span>

              <strong
                className={
                  isAvailable
                    ? "stock-positive"
                    : "stock-negative"
                }
              >
                {isAvailable
                  ? `${product.stock} in stock`
                  : "Currently unavailable"}
              </strong>
            </div>

            <div className="product-details-actions">

              <button
                type="button"
                className="secondary-button"
                onClick={onClose}
              >
                Back to products
              </button>

              <button
                type="button"
                className="approve-button"
                disabled={!isAvailable}
                onClick={() => onSelect(product)}
              >
                {isAvailable
                  ? "Select product →"
                  : "Unavailable"}
              </button>

            </div>

          </div>
        </div>
      </section>
    </div>
  );
}

export default ProductDetails;