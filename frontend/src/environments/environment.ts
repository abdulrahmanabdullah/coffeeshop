/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsnd-coffe-shop.auth0.com', // the auth0 domain prefix
    audience: 'https://coffeshop', // the audience set for the auth0 app
    clientId: '2Z3rthFn4czhpJ11PXYb8N4n9Lw1163z', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  },
};
