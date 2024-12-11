import React from 'react'
import "../css/ErrorPage.css"
import { Link } from 'react-router-dom'

function ErrorPage() {
    return (
        <div>
            <div id="err-context">
                <div id="err404"><strong><h1>404</h1></strong></div>
                <div id="errmsg-header"><h3>OOPS! PAGE NOT BE FOUND</h3></div><br />
                <div id="errmsg">Sorry but the page you are looking for does not exist, have been removed. name changed or is temporarily unavailable</div><br />
                <div id="err-action"><h4><Link to='/'>Back to Home page</Link></h4></div>
            </div>
        </div>
    )
}

export default ErrorPage