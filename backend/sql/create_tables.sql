CREATE TABLE alembic_version
(
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

CREATE TABLE sys_api
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    name         VARCHAR(50)  NOT NULL COMMENT 'apiName',
    method       VARCHAR(16)  NOT NULL COMMENT 'Request method',
    path         VARCHAR(500) NOT NULL COMMENT 'apiPath',
    remark       LONGTEXT COMMENT 'Remark',
    created_time DATETIME     NOT NULL COMMENT 'Creation time',
    updated_time DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE INDEX ix_sys_api_id ON sys_api (id);

CREATE TABLE sys_casbin_rule
(
    id    INTEGER      NOT NULL COMMENT 'primary keyid' AUTO_INCREMENT,
    ptype VARCHAR(255) NOT NULL COMMENT 'Strategy type: p or g',
    v0    VARCHAR(255) NOT NULL COMMENT 'Role / useruuid',
    v1    LONGTEXT     NOT NULL COMMENT 'apiPath / RoleName',
    v2    VARCHAR(255) COMMENT 'Request method',
    v3    VARCHAR(255),
    v4    VARCHAR(255),
    v5    VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE INDEX ix_sys_casbin_rule_id ON sys_casbin_rule (id);

CREATE TABLE sys_dept
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    name         VARCHAR(50) NOT NULL COMMENT 'departmentName',
    level        INTEGER     NOT NULL COMMENT 'Department level',
    sort         INTEGER     NOT NULL COMMENT 'Sorting',
    leader       VARCHAR(20) COMMENT 'Person in charge',
    phone        VARCHAR(11) COMMENT 'mobile phone',
    email        VARCHAR(50) COMMENT 'Email',
    status       INTEGER     NOT NULL COMMENT 'Department status(0discontinue 1Normal)',
    del_flag     BOOL        NOT NULL COMMENT 'delete(0Remove 1Existence) ',
    parent_id    INTEGER COMMENT 'father departmentID',
    created_time DATETIME    NOT NULL COMMENT 'Creation time',
    updated_time DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    FOREIGN KEY (parent_id) REFERENCES sys_dept (id) ON DELETE SET NULL
);

CREATE INDEX ix_sys_dept_id ON sys_dept (id);

CREATE INDEX ix_sys_dept_parent_id ON sys_dept (parent_id);

CREATE TABLE sys_dict_type
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    name         VARCHAR(32) NOT NULL COMMENT 'DictionaryName',
    code         VARCHAR(32) NOT NULL COMMENT 'Dictionary type code',
    status       INTEGER     NOT NULL COMMENT 'status(0discontinue 1Normal) ',
    remark       LONGTEXT COMMENT 'Remark',
    created_time DATETIME    NOT NULL COMMENT 'Creation time',
    updated_time DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    UNIQUE (code),
    UNIQUE (name)
);

CREATE INDEX ix_sys_dict_type_id ON sys_dict_type (id);

CREATE TABLE sys_login_log
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    user_uuid    VARCHAR(50)  NOT NULL COMMENT 'userUUID',
    username     VARCHAR(20)  NOT NULL COMMENT 'user',
    status       INTEGER      NOT NULL COMMENT 'loginstatus(0Failure 1Success)',
    ip           VARCHAR(50)  NOT NULL COMMENT 'loginIPAddress',
    country      VARCHAR(50) COMMENT 'Country',
    region       VARCHAR(50) COMMENT 'Area',
    city         VARCHAR(50) COMMENT 'City',
    user_agent   VARCHAR(255) NOT NULL COMMENT 'Request header',
    os           VARCHAR(50) COMMENT 'Operating System',
    browser      VARCHAR(50) COMMENT 'Browser',
    device       VARCHAR(50) COMMENT 'Equipment',
    msg          LONGTEXT     NOT NULL COMMENT 'Prompt message',
    login_time   DATETIME     NOT NULL COMMENT 'login',
    created_time DATETIME     NOT NULL COMMENT 'Creation time',
    PRIMARY KEY (id)
);

CREATE INDEX ix_sys_login_log_id ON sys_login_log (id);

CREATE TABLE sys_menu
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    title        VARCHAR(50) NOT NULL COMMENT 'Menu Title',
    name         VARCHAR(50) NOT NULL COMMENT 'MenuName',
    level        INTEGER     NOT NULL COMMENT 'Menu hierarchy',
    sort         INTEGER     NOT NULL COMMENT 'Sorting',
    icon         VARCHAR(100) COMMENT 'Menu icon',
    path         VARCHAR(200) COMMENT 'routeAddress',
    menu_type    INTEGER     NOT NULL COMMENT 'Menu type(0Table of contents 1Menu 2button) ',
    component    VARCHAR(255) COMMENT 'ComponentPath',
    perms        VARCHAR(100) COMMENT 'Authorization identifier',
    status       INTEGER     NOT NULL COMMENT 'Menustatus(0discontinue 1Normal) ',
    `show`       INTEGER     NOT NULL COMMENT 'Display(0No. 1is) ',
    cache        INTEGER     NOT NULL COMMENT 'isNo.Cache(0No. 1is) ',
    remark       LONGTEXT COMMENT 'Remark',
    parent_id    INTEGER COMMENT 'FatherMenuID',
    created_time DATETIME    NOT NULL COMMENT 'Creation time',
    updated_time DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    FOREIGN KEY (parent_id) REFERENCES sys_menu (id) ON DELETE SET NULL
);

CREATE INDEX ix_sys_menu_id ON sys_menu (id);

CREATE INDEX ix_sys_menu_parent_id ON sys_menu (parent_id);

CREATE TABLE sys_opera_log
(
    id           INTEGER      NOT NULL AUTO_INCREMENT,
    username     VARCHAR(20) COMMENT 'userName',
    method       VARCHAR(20)  NOT NULL COMMENT 'request type',
    title        VARCHAR(255) NOT NULL COMMENT 'Operation module',
    path         VARCHAR(500) NOT NULL COMMENT 'RequestPath',
    ip           VARCHAR(50)  NOT NULL COMMENT 'IPAddress',
    country      VARCHAR(50) COMMENT 'Country',
    region       VARCHAR(50) COMMENT 'Area',
    city         VARCHAR(50) COMMENT 'City',
    user_agent   VARCHAR(255) NOT NULL COMMENT 'Request header',
    os           VARCHAR(50) COMMENT 'Operating System',
    browser      VARCHAR(50) COMMENT 'Browser',
    device       VARCHAR(50) COMMENT 'Equipment',
    args         JSON COMMENT 'Request parameters',
    status       INTEGER      NOT NULL COMMENT 'Operationstatus(0abnormal 1Normal) ',
    code         VARCHAR(20)  NOT NULL COMMENT 'Operationstatuscode',
    msg          LONGTEXT COMMENT 'Prompt message',
    cost_time    FLOAT        NOT NULL COMMENT 'Request Durationms',
    opera_time   DATETIME     NOT NULL COMMENT 'operation time',
    created_time DATETIME     NOT NULL COMMENT 'Creation time',
    PRIMARY KEY (id)
);

CREATE INDEX ix_sys_opera_log_id ON sys_opera_log (id);

CREATE TABLE sys_role
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    name         VARCHAR(20) NOT NULL COMMENT 'RoleName',
    data_scope   INTEGER COMMENT 'Scope of authority(1: All data permissions 2: Custom data permissions) ',
    status       INTEGER     NOT NULL COMMENT 'Rolestatus(0discontinue 1Normal) ',
    remark       LONGTEXT COMMENT 'Remark',
    created_time DATETIME    NOT NULL COMMENT 'Creation time',
    updated_time DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE INDEX ix_sys_role_id ON sys_role (id);

CREATE TABLE sys_dict_data
(
    id           INTEGER     NOT NULL AUTO_INCREMENT,
    label        VARCHAR(32) NOT NULL COMMENT 'Dictionary Tags',
    value        VARCHAR(32) NOT NULL COMMENT 'Dictionary value.',
    sort         INTEGER     NOT NULL COMMENT 'Sorting',
    status       INTEGER     NOT NULL COMMENT 'status(0discontinue 1Normal) ',
    remark       LONGTEXT COMMENT 'Remark',
    type_id      INTEGER     NOT NULL COMMENT 'Dictionary type associationID',
    created_time DATETIME    NOT NULL COMMENT 'Creation time',
    updated_time DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    FOREIGN KEY (type_id) REFERENCES sys_dict_type (id),
    UNIQUE (label),
    UNIQUE (value)
);

CREATE INDEX ix_sys_dict_data_id ON sys_dict_data (id);

CREATE TABLE sys_role_menu
(
    id      INTEGER NOT NULL COMMENT 'primary keyID' AUTO_INCREMENT,
    role_id INTEGER NOT NULL COMMENT 'RoleID',
    menu_id INTEGER NOT NULL COMMENT 'MenuID',
    PRIMARY KEY (id, role_id, menu_id),
    FOREIGN KEY (menu_id) REFERENCES sys_menu (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES sys_role (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_sys_role_menu_id ON sys_role_menu (id);

CREATE TABLE sys_user
(
    id              INTEGER      NOT NULL AUTO_INCREMENT,
    uuid            VARCHAR(50)  NOT NULL,
    username        VARCHAR(20)  NOT NULL COMMENT 'userName',
    nickname        VARCHAR(20)  NOT NULL COMMENT 'nickname',
    password        VARCHAR(255) NOT NULL COMMENT 'Password',
    salt            VARCHAR(5)   NOT NULL COMMENT 'Salt',
    email           VARCHAR(50)  NOT NULL COMMENT 'Email',
    is_superuser    BOOL         NOT NULL COMMENT 'Super privilege(0No. 1is)',
    is_staff        BOOL         NOT NULL COMMENT 'Login for backstage management(0No. 1is)',
    status          INTEGER      NOT NULL COMMENT 'useraccountstatus(0discontinue 1Normal)',
    is_multi_login  BOOL         NOT NULL COMMENT 'isNo.Repeated login.(0No. 1is)',
    avatar          VARCHAR(255) COMMENT 'Profile picture',
    phone           VARCHAR(11) COMMENT 'mobile phonenumber',
    join_time       DATETIME     NOT NULL COMMENT 'Registration time',
    last_login_time DATETIME COMMENT 'Last timelogin',
    dept_id         INTEGER COMMENT 'Department correlationID',
    created_time    DATETIME     NOT NULL COMMENT 'Creation time',
    updated_time    DATETIME COMMENT 'Update time',
    PRIMARY KEY (id),
    FOREIGN KEY (dept_id) REFERENCES sys_dept (id) ON DELETE SET NULL,
    UNIQUE (nickname),
    UNIQUE (uuid)
);

CREATE UNIQUE INDEX ix_sys_user_email ON sys_user (email);

CREATE INDEX ix_sys_user_id ON sys_user (id);

CREATE UNIQUE INDEX ix_sys_user_username ON sys_user (username);

CREATE TABLE sys_user_role
(
    id      INTEGER NOT NULL COMMENT 'primary keyID' AUTO_INCREMENT,
    user_id INTEGER NOT NULL COMMENT 'userID',
    role_id INTEGER NOT NULL COMMENT 'RoleID',
    PRIMARY KEY (id, user_id, role_id),
    FOREIGN KEY (role_id) REFERENCES sys_role (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES sys_user (id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ix_sys_user_role_id ON sys_user_role (id);
