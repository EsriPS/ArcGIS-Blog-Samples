exports.handler = function(event, context, callback) {        
    console.log('Received event:', JSON.stringify(event, null, 2));

    // Set Values Used for Authorization
    var surveyId = process.env.surveyId;
    var portalUrl = process.env.portalUrl;

    // Retrieve request parameters from the Lambda function input:
    var headers = event.headers;

    // Perform authorization to return the Allow policy for correct parameters and 
    // the 'Unauthorized' error, otherwise.
    if (typeof headers.referer != "undefined" && headers.referer.includes(surveyId) && headers.referer.includes(portalUrl)) {
        callback(null, generateAllow('me', event.methodArn));
    }  else {
        callback("Unauthorized", generateDeny('me', event.methodArn));
    }
};
     
// Help function to generate an IAM policy
var generatePolicy = function(principalId, effect, resource) {
    // Required output:
    var authResponse = {};
    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17'; // default version
        policyDocument.Statement = [];
        var statementOne = {};
        statementOne.Action = 'execute-api:Invoke'; // default action
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }
    return authResponse;
};
     
var generateAllow = function(principalId, resource) {
    return generatePolicy(principalId, 'Allow', resource);
};

var generateDeny = function(principalId, resource) {
    return generatePolicy(principalId, 'Deny', resource);
};
