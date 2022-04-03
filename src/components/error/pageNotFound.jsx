import React from 'react';

function PageNotFound() {
    return(
    <div className="error-container-page">
      <header className="error-header">
        <div>Error 404: Not Found</div>
        <div>404 が見つかりません</div>
      </header>
      <main className="error-main">
        <h1 className="error-disclaimer">Oops! I have bad news for you</h1>
        <p className="error-message">
          The page you are looking for might be removed or temporarlily
          unavailable
        </p>
        <button>Back to Homepage</button>
      </main>
    </div>  
    )
}

export default PageNotFound
