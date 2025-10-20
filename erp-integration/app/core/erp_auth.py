"""
ERP Authentication - Sistema de autenticação e autorização para ERPs
Suporte a diferentes métodos de autenticação (OAuth2, Basic Auth, API Keys, etc.)
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import jwt
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AuthMethod(Enum):
    """Métodos de autenticação"""
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    JWT = "jwt"
    LDAP = "ldap"
    SAML = "saml"

class AuthStatus(Enum):
    """Status de autenticação"""
    AUTHENTICATED = "authenticated"
    UNAUTHENTICATED = "unauthenticated"
    EXPIRED = "expired"
    INVALID = "invalid"
    LOCKED = "locked"

@dataclass
class AuthCredentials:
    """Credenciais de autenticação"""
    username: str
    password: Optional[str] = None
    api_key: Optional[str] = None
    token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

@dataclass
class AuthResult:
    """Resultado de autenticação"""
    status: AuthStatus
    token: Optional[str] = None
    expires_at: Optional[datetime] = None
    permissions: List[str] = None
    user_info: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class ERPAuthenticator(ABC):
    """Classe base para autenticadores ERP"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_authenticated = False
        self.auth_token = None
        self.expires_at = None
        self.permissions = []
        self.user_info = {}
    
    @abstractmethod
    async def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """Autenticar usuário"""
        pass
    
    @abstractmethod
    async def refresh_token(self) -> AuthResult:
        """Renovar token"""
        pass
    
    @abstractmethod
    async def logout(self) -> bool:
        """Fazer logout"""
        pass
    
    @abstractmethod
    async def validate_token(self, token: str) -> AuthResult:
        """Validar token"""
        pass
    
    def is_token_valid(self) -> bool:
        """Verificar se token é válido"""
        if not self.is_authenticated or not self.auth_token:
            return False
        
        if self.expires_at and datetime.now() >= self.expires_at:
            return False
        
        return True

class BasicAuthAuthenticator(ERPAuthenticator):
    """Autenticador Basic Auth"""
    
    async def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """Autenticar com Basic Auth"""
        try:
            # Simulação de autenticação Basic Auth
            if credentials.username and credentials.password:
                # Hash da senha para comparação
                password_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
                
                # Simular validação (em produção, validar contra banco de dados)
                if credentials.username == "admin" and password_hash == hashlib.sha256("admin123".encode()).hexdigest():
                    self.is_authenticated = True
                    self.auth_token = secrets.token_urlsafe(32)
                    self.expires_at = datetime.now() + timedelta(hours=8)
                    self.permissions = ["read", "write", "admin"]
                    self.user_info = {
                        "username": credentials.username,
                        "role": "admin",
                        "authenticated_at": datetime.now().isoformat()
                    }
                    
                    return AuthResult(
                        status=AuthStatus.AUTHENTICATED,
                        token=self.auth_token,
                        expires_at=self.expires_at,
                        permissions=self.permissions,
                        user_info=self.user_info
                    )
                else:
                    return AuthResult(
                        status=AuthStatus.INVALID,
                        error_message="Credenciais inválidas"
                    )
            else:
                return AuthResult(
                    status=AuthStatus.INVALID,
                    error_message="Username e password são obrigatórios"
                )
                
        except Exception as e:
            logger.error(f"Erro na autenticação Basic Auth: {e}")
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message=f"Erro interno: {str(e)}"
            )
    
    async def refresh_token(self) -> AuthResult:
        """Renovar token Basic Auth"""
        if self.is_authenticated:
            self.auth_token = secrets.token_urlsafe(32)
            self.expires_at = datetime.now() + timedelta(hours=8)
            
            return AuthResult(
                status=AuthStatus.AUTHENTICATED,
                token=self.auth_token,
                expires_at=self.expires_at,
                permissions=self.permissions,
                user_info=self.user_info
            )
        else:
            return AuthResult(
                status=AuthStatus.UNAUTHENTICATED,
                error_message="Usuário não autenticado"
            )
    
    async def logout(self) -> bool:
        """Logout Basic Auth"""
        self.is_authenticated = False
        self.auth_token = None
        self.expires_at = None
        self.permissions = []
        self.user_info = {}
        return True
    
    async def validate_token(self, token: str) -> AuthResult:
        """Validar token Basic Auth"""
        if self.is_authenticated and self.auth_token == token and self.is_token_valid():
            return AuthResult(
                status=AuthStatus.AUTHENTICATED,
                token=self.auth_token,
                expires_at=self.expires_at,
                permissions=self.permissions,
                user_info=self.user_info
            )
        else:
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message="Token inválido ou expirado"
            )

class OAuth2Authenticator(ERPAuthenticator):
    """Autenticador OAuth2"""
    
    async def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """Autenticar com OAuth2"""
        try:
            if credentials.client_id and credentials.client_secret:
                # Simulação de fluxo OAuth2
                # Em produção, fazer requisição para o servidor OAuth2
                await asyncio.sleep(0.1)  # Simular latência
                
                # Simular sucesso
                self.is_authenticated = True
                self.auth_token = secrets.token_urlsafe(64)
                self.expires_at = datetime.now() + timedelta(hours=1)
                self.permissions = ["read", "write"]
                self.user_info = {
                    "client_id": credentials.client_id,
                    "scope": "erp_integration",
                    "authenticated_at": datetime.now().isoformat()
                }
                
                return AuthResult(
                    status=AuthStatus.AUTHENTICATED,
                    token=self.auth_token,
                    expires_at=self.expires_at,
                    permissions=self.permissions,
                    user_info=self.user_info
                )
            else:
                return AuthResult(
                    status=AuthStatus.INVALID,
                    error_message="Client ID e Client Secret são obrigatórios"
                )
                
        except Exception as e:
            logger.error(f"Erro na autenticação OAuth2: {e}")
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message=f"Erro interno: {str(e)}"
            )
    
    async def refresh_token(self) -> AuthResult:
        """Renovar token OAuth2"""
        if self.is_authenticated:
            # Simular renovação de token OAuth2
            await asyncio.sleep(0.1)
            
            self.auth_token = secrets.token_urlsafe(64)
            self.expires_at = datetime.now() + timedelta(hours=1)
            
            return AuthResult(
                status=AuthStatus.AUTHENTICATED,
                token=self.auth_token,
                expires_at=self.expires_at,
                permissions=self.permissions,
                user_info=self.user_info
            )
        else:
            return AuthResult(
                status=AuthStatus.UNAUTHENTICATED,
                error_message="Usuário não autenticado"
            )
    
    async def logout(self) -> bool:
        """Logout OAuth2"""
        # Simular revogação de token
        await asyncio.sleep(0.1)
        
        self.is_authenticated = False
        self.auth_token = None
        self.expires_at = None
        self.permissions = []
        self.user_info = {}
        return True
    
    async def validate_token(self, token: str) -> AuthResult:
        """Validar token OAuth2"""
        if self.is_authenticated and self.auth_token == token and self.is_token_valid():
            return AuthResult(
                status=AuthStatus.AUTHENTICATED,
                token=self.auth_token,
                expires_at=self.expires_at,
                permissions=self.permissions,
                user_info=self.user_info
            )
        else:
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message="Token inválido ou expirado"
            )

class APIKeyAuthenticator(ERPAuthenticator):
    """Autenticador API Key"""
    
    async def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """Autenticar com API Key"""
        try:
            if credentials.api_key:
                # Simular validação de API Key
                valid_api_keys = {
                    "sk-1234567890abcdef": {"permissions": ["read", "write"], "user": "admin"},
                    "sk-abcdef1234567890": {"permissions": ["read"], "user": "user"}
                }
                
                if credentials.api_key in valid_api_keys:
                    api_key_info = valid_api_keys[credentials.api_key]
                    
                    self.is_authenticated = True
                    self.auth_token = credentials.api_key
                    self.expires_at = datetime.now() + timedelta(days=30)  # API Keys duram mais
                    self.permissions = api_key_info["permissions"]
                    self.user_info = {
                        "api_key": credentials.api_key,
                        "user": api_key_info["user"],
                        "authenticated_at": datetime.now().isoformat()
                    }
                    
                    return AuthResult(
                        status=AuthStatus.AUTHENTICATED,
                        token=self.auth_token,
                        expires_at=self.expires_at,
                        permissions=self.permissions,
                        user_info=self.user_info
                    )
                else:
                    return AuthResult(
                        status=AuthStatus.INVALID,
                        error_message="API Key inválida"
                    )
            else:
                return AuthResult(
                    status=AuthStatus.INVALID,
                    error_message="API Key é obrigatória"
                )
                
        except Exception as e:
            logger.error(f"Erro na autenticação API Key: {e}")
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message=f"Erro interno: {str(e)}"
            )
    
    async def refresh_token(self) -> AuthResult:
        """Renovar token API Key (não aplicável)"""
        return AuthResult(
            status=AuthStatus.AUTHENTICATED,
            token=self.auth_token,
            expires_at=self.expires_at,
            permissions=self.permissions,
            user_info=self.user_info
        )
    
    async def logout(self) -> bool:
        """Logout API Key"""
        self.is_authenticated = False
        self.auth_token = None
        self.expires_at = None
        self.permissions = []
        self.user_info = {}
        return True
    
    async def validate_token(self, token: str) -> AuthResult:
        """Validar token API Key"""
        if self.is_authenticated and self.auth_token == token and self.is_token_valid():
            return AuthResult(
                status=AuthStatus.AUTHENTICATED,
                token=self.auth_token,
                expires_at=self.expires_at,
                permissions=self.permissions,
                user_info=self.user_info
            )
        else:
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message="API Key inválida ou expirada"
            )

class JWTAuthenticator(ERPAuthenticator):
    """Autenticador JWT"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.secret_key = config.get("secret_key", "your-secret-key")
        self.algorithm = config.get("algorithm", "HS256")
    
    async def authenticate(self, credentials: AuthCredentials) -> AuthResult:
        """Autenticar com JWT"""
        try:
            if credentials.username and credentials.password:
                # Simular validação de credenciais
                if credentials.username == "admin" and credentials.password == "admin123":
                    # Gerar JWT
                    payload = {
                        "username": credentials.username,
                        "role": "admin",
                        "permissions": ["read", "write", "admin"],
                        "exp": datetime.now() + timedelta(hours=8),
                        "iat": datetime.now()
                    }
                    
                    token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
                    
                    self.is_authenticated = True
                    self.auth_token = token
                    self.expires_at = datetime.fromtimestamp(payload["exp"])
                    self.permissions = payload["permissions"]
                    self.user_info = {
                        "username": credentials.username,
                        "role": "admin",
                        "authenticated_at": datetime.now().isoformat()
                    }
                    
                    return AuthResult(
                        status=AuthStatus.AUTHENTICATED,
                        token=self.auth_token,
                        expires_at=self.expires_at,
                        permissions=self.permissions,
                        user_info=self.user_info
                    )
                else:
                    return AuthResult(
                        status=AuthStatus.INVALID,
                        error_message="Credenciais inválidas"
                    )
            else:
                return AuthResult(
                    status=AuthStatus.INVALID,
                    error_message="Username e password são obrigatórios"
                )
                
        except Exception as e:
            logger.error(f"Erro na autenticação JWT: {e}")
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message=f"Erro interno: {str(e)}"
            )
    
    async def refresh_token(self) -> AuthResult:
        """Renovar token JWT"""
        if self.is_authenticated:
            try:
                # Decodificar token atual
                payload = jwt.decode(self.auth_token, self.secret_key, algorithms=[self.algorithm])
                
                # Gerar novo token
                new_payload = {
                    "username": payload["username"],
                    "role": payload["role"],
                    "permissions": payload["permissions"],
                    "exp": datetime.now() + timedelta(hours=8),
                    "iat": datetime.now()
                }
                
                self.auth_token = jwt.encode(new_payload, self.secret_key, algorithm=self.algorithm)
                self.expires_at = datetime.fromtimestamp(new_payload["exp"])
                
                return AuthResult(
                    status=AuthStatus.AUTHENTICATED,
                    token=self.auth_token,
                    expires_at=self.expires_at,
                    permissions=self.permissions,
                    user_info=self.user_info
                )
            except jwt.ExpiredSignatureError:
                return AuthResult(
                    status=AuthStatus.EXPIRED,
                    error_message="Token expirado"
                )
            except jwt.InvalidTokenError:
                return AuthResult(
                    status=AuthStatus.INVALID,
                    error_message="Token inválido"
                )
        else:
            return AuthResult(
                status=AuthStatus.UNAUTHENTICATED,
                error_message="Usuário não autenticado"
            )
    
    async def logout(self) -> bool:
        """Logout JWT"""
        self.is_authenticated = False
        self.auth_token = None
        self.expires_at = None
        self.permissions = []
        self.user_info = {}
        return True
    
    async def validate_token(self, token: str) -> AuthResult:
        """Validar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            return AuthResult(
                status=AuthStatus.AUTHENTICATED,
                token=token,
                expires_at=datetime.fromtimestamp(payload["exp"]),
                permissions=payload.get("permissions", []),
                user_info={
                    "username": payload["username"],
                    "role": payload["role"]
                }
            )
        except jwt.ExpiredSignatureError:
            return AuthResult(
                status=AuthStatus.EXPIRED,
                error_message="Token expirado"
            )
        except jwt.InvalidTokenError:
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message="Token inválido"
            )

class ERPAuthManager:
    """Gerenciador de autenticação ERP"""
    
    def __init__(self):
        self.authenticators: Dict[str, ERPAuthenticator] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def register_authenticator(self, erp_type: str, auth_method: AuthMethod, config: Dict[str, Any]) -> ERPAuthenticator:
        """Registrar autenticador para ERP"""
        authenticator_classes = {
            AuthMethod.BASIC_AUTH: BasicAuthAuthenticator,
            AuthMethod.OAUTH2: OAuth2Authenticator,
            AuthMethod.API_KEY: APIKeyAuthenticator,
            AuthMethod.JWT: JWTAuthenticator
        }
        
        if auth_method not in authenticator_classes:
            raise ValueError(f"Método de autenticação não suportado: {auth_method}")
        
        authenticator = authenticator_classes[auth_method](config)
        key = f"{erp_type}_{auth_method.value}"
        self.authenticators[key] = authenticator
        
        return authenticator
    
    async def authenticate(self, erp_type: str, auth_method: AuthMethod, credentials: AuthCredentials) -> AuthResult:
        """Autenticar usuário"""
        key = f"{erp_type}_{auth_method.value}"
        
        if key not in self.authenticators:
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message=f"Autenticador não encontrado para {erp_type} com {auth_method.value}"
            )
        
        authenticator = self.authenticators[key]
        result = await authenticator.authenticate(credentials)
        
        if result.status == AuthStatus.AUTHENTICATED:
            # Registrar sessão ativa
            session_id = secrets.token_urlsafe(32)
            self.active_sessions[session_id] = {
                "erp_type": erp_type,
                "auth_method": auth_method.value,
                "authenticator": authenticator,
                "created_at": datetime.now(),
                "last_activity": datetime.now()
            }
            result.user_info["session_id"] = session_id
        
        return result
    
    async def validate_session(self, session_id: str) -> AuthResult:
        """Validar sessão"""
        if session_id not in self.active_sessions:
            return AuthResult(
                status=AuthStatus.INVALID,
                error_message="Sessão não encontrada"
            )
        
        session = self.active_sessions[session_id]
        authenticator = session["authenticator"]
        
        if not authenticator.is_token_valid():
            # Remover sessão expirada
            del self.active_sessions[session_id]
            return AuthResult(
                status=AuthStatus.EXPIRED,
                error_message="Sessão expirada"
            )
        
        # Atualizar última atividade
        session["last_activity"] = datetime.now()
        
        return AuthResult(
            status=AuthStatus.AUTHENTICATED,
            token=authenticator.auth_token,
            expires_at=authenticator.expires_at,
            permissions=authenticator.permissions,
            user_info=authenticator.user_info
        )
    
    async def logout_session(self, session_id: str) -> bool:
        """Fazer logout da sessão"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            authenticator = session["authenticator"]
            await authenticator.logout()
            del self.active_sessions[session_id]
            return True
        return False
    
    def get_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Obter sessões ativas"""
        return self.active_sessions.copy()
    
    def cleanup_expired_sessions(self):
        """Limpar sessões expiradas"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            authenticator = session["authenticator"]
            if not authenticator.is_token_valid():
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
        
        logger.info(f"Removidas {len(expired_sessions)} sessões expiradas")

