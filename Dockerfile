FROM nodered/node-red

COPY /node-red/package.json .
RUN npm install 

RUN touch soil_data_9

COPY /node-red/settings.js /data/settings.js
COPY /node-red/flows_cred.json /data/flows_cred.json
COPY /node-red/flows.json /data/flows.json

EXPOSE 1880