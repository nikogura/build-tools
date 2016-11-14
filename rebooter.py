import requests
import xmltodict

class Rebooter:
    '''
    https://teamcity-qa.apple.com/agentDetails.html?id=9960&agentTypeId=33&realAgentName=iossys-agent-1493#
    curl -u User:Password -X POST "http://MyTeamCityServerURL/remoteAccess/reboot.html?agent=2&rebootAfterBuild=true"

    curl -s teamcityServer/guestAuth/app/rest/agents | xmlstarlet sel -t -v '//agents/agent[@name="YOUR_AGENT_NAME"]/@id'


    agent name from param
      get agent ID
      /httpAuth/app/rest/agents/id:<id>


    '''

    def __init__(self, server, username, password):
        self._server = server
        self._username = username
        self._password = password
        self._path_prefix = "httpAuth/app/rest"

    @property
    def server(self):
        return self._server

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def path_prefix(self):
        return self._path_prefix

    def get_agents(self):
        url = "%s/%s/%s" % (self.server, self.path_prefix, 'agents')

        resp = requests.get('https://teamcity-qa.apple.com/httpAuth/app/rest/agents', auth=(self.username, self.password))

        data = xmltodict.parse(resp.content)
        agents = []

        for agent in data.get('agents').get('agent'):
            agent = Agent(
                id=agent.get('@id'),
                name=agent.get('@name'),
                typeId=agent.get('@typeId'),
                href=agent.get('@href')
            )

            agents.append(agent)

        return agents

    def reboot_agent(self, agent_id):
        url = "%s/httpAuth/remoteAccess/reboot.html" % self.server
        payload = {'agent': agent_id, 'rebootAfterBuild': False}

        resp = requests.post(url, payload, auth=(self.username, self.password))

        return resp

class Agent:
    def __init__(self, id, name, typeId, href):
        self._id = id
        self._name = name
        self._typeId = typeId
        self._href = href

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__hash__ == other.__hash__

    def __hash__(self):
        return hash(str(self))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def typeId(self):
        return self._typeId

    @property
    def href(self):
        return self._href

if __name__ == '__main__':
    pass