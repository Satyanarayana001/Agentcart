function AlternativeProducts({
  unavailableProduct,
  alternatives,
  onSelect,
}) {
  if (
    !unavailableProduct ||
    !alternatives ||
    alternatives.length === 0
  ) {
    return null;
  }

  return (
    <section className="alternatives-section">

      <div className="section-label">
        PRODUCT UNAVAILABLE
      </div>

      <div className="alternatives-header">
        <div>
          <h2>
            {unavailableProduct.name} is unavailable
          </h2>

          <p>
            AgentCart found available alternatives.
            Choose one to continue. Your selection is
            required before a purchase plan is created.
          </p>
        </div>

        <span className="unavailable-badge">
          Out of stock
        </span>
      </div>

      <div className="alternatives-grid">
        {alternatives.map((product) => (
          <article
            className="alternative-card"
            key={product.product_id}
          >
            <div className="alternative-card-top">
              <div className="alternative-icon">
                {product.name
                  .toLowerCase()
                  .includes("case")
                  ? "▣"
                  : "🎧"}
              </div>

              <span className="alternative-stock">
                {product.stock} available
              </span>
            </div>

            <div className="product-category">
              Alternative
            </div>

            <h3>{product.name}</h3>

            <p>
              {product.description}
            </p>

            <div className="alternative-price">
              ₹
              {Number(product.price).toLocaleString(
                "en-IN"
              )}
            </div>

            <div className="alternative-reason">
              <span>WHY THIS OPTION</span>

              <p>{product.reason}</p>
            </div>

            <button
              type="button"
              className="approve-button"
              onClick={() => onSelect(product)}
              disabled={false}
            >
              Choose this product →
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}

export default AlternativeProducts;