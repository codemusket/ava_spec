openapi: 3.0.3
info:
  title: Ava Protocol EigenLayer AVS API
  version: 1.0.0
  description: |
    Note: Unofficial. Not affiliated with Ava Protocol.
    Comprehensive guide to working with gRPC endpoints and API references for the Ava Protocol EigenLayer AVS, including authentication and API methods.

servers:
  - url: grpc://aggregator.avaprotocol.org:2206
    description: Ethereum Mainnet
  - url: grpc://aggregator-holesky.avaprotocol.org:2206
    description: Holesky Testnet
  - url: grpc://127.0.0.1:2206
    description: Local Development

paths:
  /GetSmartAccountAddress:
    post:
      summary: Retrieve Smart Account Address
      operationId: GetSmartAccountAddress
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddressRequest'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AddressResp'

  /CreateTask:
    post:
      summary: Create a New Task
      operationId: CreateTask
      security:
        - AuthKey: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskReq'
      responses:
        '200':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateTaskResp'

  /ListTasks:
    get:
      summary: List Tasks
      operationId: ListTasks
      security:
        - AuthKey: []
      responses:
        '200':
          description: List of tasks
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListTasksResp'

  /CancelTask:
    post:
      summary: Cancel a Task
      operationId: CancelTask
      security:
        - AuthKey: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskIdRequest'
      responses:
        '200':
          description: Cancellation status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BoolValue'

  /DeleteTask:
    post:
      summary: Delete a Task
      operationId: DeleteTask
      security:
        - AuthKey: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskIdRequest'
      responses:
        '200':
          description: Deletion status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BoolValue'

  /GetKey:
    post:
      summary: Exchange for an Auth Token
      operationId: GetKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GetKeyRequest'
      responses:
        '200':
          description: Auth key obtained successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetKeyResponse'

components:
  securitySchemes:
    AuthKey:
      type: apiKey
      in: header
      name: authkey

  schemas:
    AddressRequest:
      type: object
      properties:
        owner:
          type: string
          description: The hex address of the account owner whose smart wallet address is being requested.
      required:
        - owner

    AddressResp:
      type: object
      properties:
        smart_account_address:
          type: string
          description: The retrieved smart wallet address for the specified owner.
        nonce:
          type: string
          description: The current nonce of the smart wallet.

    CreateTaskReq:
      type: object
      properties:
        task_type:
          $ref: '#/components/schemas/TaskType'
        action:
          $ref: '#/components/schemas/TaskAction'
        trigger:
          $ref: '#/components/schemas/TaskTrigger'
        start_at:
          type: integer
          format: int64
          description: The epoch time (in seconds) after which the task becomes valid.
        expired_at:
          type: integer
          format: int64
          description: The epoch time (in seconds) after which the task is no longer valid.
        memo:
          type: string
          description: Optional field to store arbitrary notes or metadata related to the task.
      required:
        - task_type
        - action
        - trigger

    CreateTaskResp:
      type: object
      properties:
        id:
          type: string
          description: The unique identifier of the created task.

    ListTasksResp:
      type: object
      properties:
        tasks:
          type: array
          items:
            $ref: '#/components/schemas/TaskItemResp'

    TaskItemResp:
      type: object
      properties:
        id:
          type: string
          description: The unique identifier of the task.
        status:
          $ref: '#/components/schemas/TaskStatus'

    TaskIdRequest:
      type: object
      properties:
        id:
          type: string
          description: The unique identifier of the task.
      required:
        - id

    GetKeyRequest:
      type: object
      properties:
        owner:
          type: string
          description: Your wallet address.
        expired_at:
          type: integer
          format: int64
          description: The epoch time when your key will expire.
        signature:
          type: string
          description: Signature of the message.
      required:
        - owner
        - expired_at
        - signature

    GetKeyResponse:
      type: object
      properties:
        key:
          type: string
          description: The authentication key to be used in subsequent requests.

    BoolValue:
      type: object
      properties:
        value:
          type: boolean
          description: Indicates whether the operation was successful (true) or not (false).

    TaskType:
      type: string
      enum:
        - ETHTransferTask
        - ContractExecutionTask
      description: The type of task to create.

    TaskStatus:
      type: string
      enum:
        - Active
        - Completed
        - Failed
        - Canceled
      description: The current status of the task.

    TaskAction:
      type: object
      description: Union type for different task actions.
      oneOf:
        - $ref: '#/components/schemas/ETHTransfer'
        - $ref: '#/components/schemas/ContractExecution'

    ETHTransfer:
      type: object
      properties:
        destination:
          type: string
          description: The hex string address of the recipient.
        amount:
          type: string
          description: The hex string of ETH amount.
      required:
        - destination
        - amount

    ContractExecution:
      type: object
      properties:
        contract_address:
          type: string
          description: The target contract address in hex.
        calldata:
          type: string
          description: The encoded contract method and its arguments.
        method:
          type: string
          description: Optional - only used for display/format purposes.
        encoded_params:
          type: string
          description: Optional - only used for display/format purposes.
      required:
        - contract_address
        - calldata

    TaskTrigger:
      type: object
      description: Union type for different trigger conditions.
      properties:
        trigger_type:
          $ref: '#/components/schemas/TriggerType'
      oneOf:
        - $ref: '#/components/schemas/Schedule'
        - $ref: '#/components/schemas/ContractQuery'
        - $ref: '#/components/schemas/Expression'

    TriggerType:
      type: string
      enum:
        - TimeCondition
        - ContractQueryCondition
        - ExpressionCondition
      description: The type of trigger condition.

    Schedule:
      type: object
      properties:
        fixed:
          type: array
          items:
            type: integer
            format: int64
          description: A list of epoch timestamps when the task can be triggered.
        cron:
          type: string
          description: A crontab expression representing when the task can be triggered.

    ContractQuery:
      type: object
      properties:
        contract_address:
          type: string
          description: Target contract address in hex format.
        callmsg:
          type: string
          description: Encoded payload in hex format to send to the contract.
      required:
        - contract_address
        - callmsg

    Expression:
      type: object
      properties:
        expression:
          type: string
          description: The raw expression to be evaluated.

security:
  - AuthKey: []
