package com.armareforger.tacmap.data.models

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "users")
data class User(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val username: String,
    val passwordHash: String,
    val totpSecret: String? = null,
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "markers")
data class Marker(
    @PrimaryKey
    val id: String,
    val type: MarkerType,
    val shape: MarkerShape,
    val x: Float,
    val y: Float,
    val color: String,
    val createdBy: String,
    val timestamp: Long = System.currentTimeMillis(),
    val notes: String? = null
)

enum class MarkerType {
    ENEMY, FRIENDLY, ATTACK, DEFEND,
    PICKUP, DROP, MEET, INFANTRY,
    ARMOR, AIR, NAVAL, OBJECTIVE, OTHER
}

enum class MarkerShape {
    CIRCLE, SQUARE, DIAMOND, TRIANGLE,
    ARROW, STAR, POLYGON
}

@Entity(tableName = "servers")
data class Server(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val name: String,
    val ipAddress: String,
    val port: Int,
    val enabled: Boolean = true
)

@Entity(tableName = "sessions")
data class Session(
    @PrimaryKey
    val token: String,
    val userId: Int,
    val deviceId: String,
    val expiresAt: Long
)

@Entity(tableName = "feedback")
data class Feedback(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val type: FeedbackType,
    val message: String,
    val email: String? = null,
    val submittedAt: Long = System.currentTimeMillis()
)

enum class FeedbackType {
    BUG, FEATURE, SUGGESTION
}

// WebSocket message models
data class WebSocketMessage(
    val type: String,
    val action: String? = null,
    val data: Any? = null,
    val timestamp: Long = System.currentTimeMillis()
)

data class WSStatus(
    val connected: Boolean,
    val clients: Int,
    val port: Int
)
